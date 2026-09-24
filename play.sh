#!/usr/bin/env bash
# Bad Apple!! played by `git log`.
#
# Every commit in this repository is one frame of the video: the frame is
# the commit message body, and `screen.txt` holds the same frame in the tree.
# This script does nothing but stream `git log` to the terminal at 30 fps.
#
#   ./play.sh              play from the first frame
#   FPS=15 ./play.sh       slow motion
set -u
cd "$(dirname "$0")" || exit 1

FPS=${FPS:-30}
ROWS=30
COLS=80

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "play.sh 需要在 git clone 下來的倉庫裡執行（每一幀都存在 commit 裡）。" >&2
  exit 1
fi

term_cols=$(tput cols 2>/dev/null || echo "$COLS")
term_lines=$(tput lines 2>/dev/null || echo $((ROWS + 1)))
if (( term_cols < COLS || term_lines < ROWS + 1 )); then
  printf '終端機至少要 %dx%d（目前 %dx%d），畫面可能會亂掉。按 Enter 繼續… ' \
    "$COLS" $((ROWS + 1)) "$term_cols" "$term_lines"
  read -r _
fi

finish() {
  printf '\e[0m\e[%d;1H\e[?25h\n' $((ROWS + 2))
  exit
}
trap finish INT TERM
printf '\e[?25l\e[2J'

frame_us=$((1000000 / FPS))
have_clock=0
[[ -n ${EPOCHREALTIME:-} ]] && have_clock=1   # bash 5+; otherwise fixed sleeps
printf -v fixed_sleep '0.%06d' "$frame_us"

i=0
dropped=0
while IFS= read -r -d $'\x1e' rec || [[ -n $rec ]]; do
  [[ -z $rec ]] && continue
  subject=${rec%%$'\n'*}
  body=${rec#*$'\n'}
  frame=${body%%$'\n\n'*}   # the frame ends at the blank line before the trailers

  if (( have_clock )); then
    now=${EPOCHREALTIME/[.,]/}
    (( i == 0 )) && start=$now
    target=$((start + i * frame_us))
    i=$((i + 1))
    if (( now > target + frame_us )); then   # running late: drop this frame
      dropped=$((dropped + 1))
      continue
    fi
    if (( now < target )); then
      d=$((target - now))
      printf -v s '%d.%06d' $((d / 1000000)) $((d % 1000000))
      sleep "$s"
    fi
  else
    sleep "$fixed_sleep"
  fi

  printf '\e[H%s\n\e[7m %-*s\e[0m' "$frame" $((COLS - 1)) "▶ Bad Apple!! on git · $subject"
done < <(git --no-pager log --reverse --grep='^frame [0-9]' --format='%x1e%s%n%b')

(( dropped > 0 )) && printf '\e[%d;1H（掉了 %d 幀，終端機跟不上 %d fps）' $((ROWS + 2)) "$dropped" "$FPS"
finish
