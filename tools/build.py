#!/usr/bin/env python3
"""Turn the Bad Apple!! PV into git history: one commit per frame.

    python3 tools/build.py badapple.mp4 | git fast-import

Each frame is downscaled to 80x60 pixels, thresholded to black and white,
and drawn with half-block characters (two pixel rows per text row), giving
an 80x30 text frame. That frame becomes both the body of a commit message
and the contents of screen.txt, and the commits are appended to the current
branch, one second apart.

Needs numpy and ffmpeg (on PATH, or via `pip install imageio-ffmpeg`).
"""
import argparse
import shutil
import subprocess
import sys

import numpy as np

BLOCKS = np.array([" ", "▄", "▀", "█"])  # index = top * 2 + bottom


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def read_frames(video, width, height, fps):
    raw = subprocess.run(
        [ffmpeg_exe(), "-loglevel", "error", "-i", video,
         "-vf", f"fps={fps},scale={width}:{height}:flags=area,format=gray",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"],
        check=True, stdout=subprocess.PIPE,
    ).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, height, width) >= 128


def render(pixels):
    top, bottom = pixels[0::2].astype(int), pixels[1::2].astype(int)
    return "\n".join("".join(row) for row in BLOCKS[top * 2 + bottom]) + "\n"


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def data(text):
    b = text.encode()
    return b"data %d\n%s\n" % (len(b), b)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("--width", type=int, default=80)
    p.add_argument("--rows", type=int, default=30, help="text rows per frame")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--trailer", action="append", default=[],
                   help="trailer line appended to every commit message")
    args = p.parse_args()

    branch = git("symbolic-ref", "--short", "HEAD")
    parent_time = int(git("log", "-1", "--format=%ct"))
    tz = git("log", "-1", "--format=%ci").split()[-1]
    ident = f"{git('config', 'user.name')} <{git('config', 'user.email')}>"

    frames = read_frames(args.video, args.width, args.rows * 2, args.fps)
    n = len(frames)
    trailers = "".join(t + "\n" for t in args.trailer)
    out = sys.stdout.buffer

    for i, pixels in enumerate(frames):
        screen = render(pixels)
        t_ms = i * 1000 // args.fps
        subject = f"frame {i + 1:04d}/{n} {t_ms // 60000:02d}:{t_ms // 1000 % 60:02d}.{t_ms % 1000:03d}"
        message = f"{subject}\n\n{screen}" + (f"\n{trailers}" if trailers else "")
        when = f"{parent_time + i + 1} {tz}"
        out.write(f"commit refs/heads/{branch}\n".encode())
        out.write(f"author {ident} {when}\ncommitter {ident} {when}\n".encode())
        out.write(data(message))
        if i == 0:
            out.write(f"from refs/heads/{branch}^0\n".encode())
        out.write(b"M 100644 inline screen.txt\n" + data(screen))
    print(f"{n} frames", file=sys.stderr)


if __name__ == "__main__":
    main()
