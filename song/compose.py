#!/usr/bin/env python3
"""夕焼けシグナル (vocal version) — the score.

An anime-opening style J-pop song in E major at 172 BPM, about 80 seconds
(TV size). This file holds everything that is composed: chords, the vocal
line with its lyrics, and every instrument part. It writes

    out/vocal.musicxml   the vocal line with lyrics (for the singing synthesizer)
    out/<stem>.mid       one MIDI file per instrument group (for FluidSynth)

Grid: durations are in eighth notes, 8 per bar of 4/4.
"""
import os
import random

import pretty_midi

BPM = 172
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
random.seed(7)

# ---------------------------------------------------------------- harmony
# one chord per bar; a tuple splits the bar in half
INTRO = ["A", "B", "G#m", "C#m", "A", "B", "E", "E"]
VERSE = ["C#m", "A", "B", "E", "C#m", "A", "B", "B"]
VERSE2 = ["C#m", "A", "B", "G#m", "A", "F#m", "B", "B"]
PRE = ["AM7", "G#7", "C#m7", ("Bm7", "E7"), "AM7", "G#7", "C#m7", "B"]          # 丸サ進行, then V
CHORUS = ["A", "B", "G#m", "C#m", "A", "B", "E", "E",                         # 王道進行 IV–V–iii–vi
          "A", "B", "G#m", "C#m", "F#m", "G#m", "A", "B"]
OUTRO = ["E", "E", "A", "B", "G#m", "C#m", ("A", "B"), "E"]
SECTIONS = [("intro", INTRO), ("verse", VERSE), ("verse2", VERSE2), ("pre", PRE),
            ("chorus", CHORUS), ("outro", OUTRO)]
BARS = [c for _, sec in SECTIONS for c in sec]
START = {}
_b = 0
for name, sec in SECTIONS:
    START[name] = _b
    _b += len(sec)
N_BARS = _b

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
QUALITY = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "M7": [0, 4, 7, 11], "m7": [0, 3, 7, 10]}


def chord_tones(sym):
    root = NOTE[sym[0]] + (1 if sym[1:2] == "#" else -1 if sym[1:2] == "b" else 0)
    qual = sym[1 + (sym[1:2] in "#b" and len(sym) > 1):]
    return root % 12, [(root + i) % 12 for i in QUALITY[qual]]


def chords_in_bar(bar):
    c = BARS[bar]
    return [(0, 8, c)] if isinstance(c, str) else [(0, 4, c[0]), (4, 8, c[1])]


def midi(name):
    step = NOTE[name[0]]
    rest = name[1:]
    while rest and rest[0] in "#b":
        step += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    return 12 * (int(rest) + 1) + step


# ---------------------------------------------------------------- vocal
# (pitch or None, eighths, lyric). One kana per note; へ is written え as sung.
_ = None
VOCAL = {
    # A: 夕焼け空に / 光る印を / いつも探して / 君を呼んでた
    "verse": [
        (_, 1, _), ("G#4", 1, "ゆ"), ("G#4", 1, "う"), ("G#4", 1, "や"), ("F#4", 1, "け"), ("G#4", 2, "そ"), ("B4", 1, "ら"),
        ("C#5", 3, "に"), (_, 2, _), ("B4", 1, "ひ"), ("C#5", 1, "か"), ("B4", 1, "る"),
        ("B4", 2, "し"), ("A4", 1, "る"), ("G#4", 1, "し"), ("F#4", 2, "を"), (_, 2, _),
        (_, 5, _), ("G#4", 1, "い"), ("G#4", 1, "つ"), ("A4", 1, "も"),
        ("G#4", 2, "さ"), ("F#4", 1, "が"), ("E4", 1, "し"), ("F#4", 2, "て"), (_, 2, _),
        (_, 1, _), ("E4", 1, "き"), ("F#4", 1, "み"), ("G#4", 1, "を"), ("A4", 2, "よ"), ("G#4", 1, "ん"), ("F#4", 1, "で"),
        ("F#4", 4, "た"), (_, 4, _),
        (_, 5, _), ("B4", 1, "と"), ("B4", 1, "ど"), ("C#5", 1, "か"),
    ],
    # A': 届かない声も / 重ねた夢も / 今日の風に / 乗せていくよ
    "verse2": [
        ("C#5", 2, "な"), ("B4", 1, "い"), (_, 1, _), ("G#4", 1, "こ"), ("B4", 1, "え"), ("C#5", 2, "も"),
        (_, 1, _), ("C#5", 1, "か"), ("C#5", 1, "さ"), ("B4", 1, "ね"), ("A4", 2, "た"), ("G#4", 1, "ゆ"), ("A4", 1, "め"),
        ("B4", 4, "も"), (_, 4, _),
        (_, 2, _), ("B4", 1, "きょ"), ("B4", 1, "う"), ("D#5", 2, "の"), ("C#5", 1, "か"), ("B4", 1, "ぜ"),
        ("C#5", 3, "に"), (_, 1, _), ("C#5", 1, "の"), ("B4", 1, "せ"), ("A4", 1, "て"), (_, 1, _),
        ("A4", 2, "い"), ("B4", 1, "く"), ("C#5", 5, "よ"),
        (_, 8, _),
        (_, 6, _), ("G#4", 1, "ま"), ("A4", 1, "よ"),
    ],
    # B: 迷いながら / それでも前に / 震える手を / 握りしめて / 今こそ
    "pre": [
        ("G#4", 3, "い"), ("E4", 1, "な"), ("F#4", 1, "が"), ("G#4", 3, "ら"),
        (_, 1, _), ("D#5", 1, "そ"), ("D#5", 1, "れ"), ("C5", 1, "で"), ("D#5", 2, "も"), (_, 2, _),
        ("E5", 2, "ま"), ("D#5", 1, "え"), ("C#5", 4, "に"), (_, 1, _),
        (_, 2, _), ("D5", 1, "ふ"), ("C#5", 1, "る"), ("B4", 1, "え"), ("D5", 1, "る"), ("E5", 2, "て"),
        ("C#5", 4, "を"), (_, 2, _), ("G#4", 1, "に"), ("A4", 1, "ぎ"),
        ("C5", 2, "り"), ("D#5", 1, "し"), ("C5", 1, "め"), ("G#4", 4, "て"),
        (_, 8, _),
        (_, 4, _), ("B4", 1, "い"), ("C#5", 1, "ま"), ("D#5", 1, "こ"), ("E5", 1, "そ"),
    ],
    # サビ: 届け夕焼けシグナル / 赤く燃える空へ / 何度負けても / 君がいるなら
    #       届け僕らのシグナル / 夜が来る前に / この声枯れるまで / 歌い続けるよ
    "chorus": [
        ("E5", 2, "と"), ("D#5", 1, "ど"), ("E5", 3, "け"), ("C#5", 1, "ゆ"), ("B4", 1, "う"),
        ("B4", 1, "や"), ("C#5", 1, "け"), ("D#5", 2, "し"), ("F#5", 1, "ぐ"), ("D#5", 1, "な"), ("B4", 2, "る"),
        (_, 1, _), ("B4", 1, "あ"), ("B4", 1, "か"), ("D#5", 1, "く"), ("D#5", 2, "も"), ("C#5", 1, "え"), ("B4", 1, "る"),
        ("C#5", 1, "そ"), ("B4", 1, "ら"), ("G#4", 6, "え"),
        (_, 1, _), ("E5", 1, "な"), ("E5", 1, "ん"), ("E5", 1, "ど"), ("F#5", 2, "ま"), ("E5", 1, "け"), ("C#5", 1, "て"),
        ("D#5", 4, "も"), (_, 2, _), ("B4", 1, "き"), ("C#5", 1, "み"),
        ("E5", 2, "が"), (_, 1, _), ("B4", 1, "い"), ("C#5", 1, "る"), ("B4", 1, "な"), ("G#4", 2, "ら"),
        (_, 6, _), ("B4", 1, "と"), ("C#5", 1, "ど"),
        ("E5", 3, "け"), ("C#5", 1, "ぼ"), ("E5", 2, "く"), ("F#5", 1, "ら"), ("E5", 1, "の"),
        ("D#5", 1, "し"), ("E5", 1, "ぐ"), ("F#5", 2, "な"), ("D#5", 4, "る"),
        (_, 1, _), ("D#5", 1, "よ"), ("D#5", 1, "る"), ("B4", 1, "が"), ("D#5", 1, "く"), ("E5", 1, "る"), ("D#5", 1, "ま"), ("B4", 1, "え"),
        ("C#5", 4, "に"), (_, 4, _),
        (_, 1, _), ("A4", 1, "こ"), ("B4", 1, "の"), ("C#5", 2, "こ"), ("B4", 1, "え"), ("A4", 1, "か"), ("C#5", 1, "れ"),
        ("B4", 2, "る"), ("B4", 1, "ま"), ("D#5", 5, "で"),
        (_, 1, _), ("C#5", 1, "う"), ("C#5", 1, "た"), ("E5", 1, "い"), ("E5", 2, "つ"), ("E5", 1, "づ"), ("F#5", 1, "け"),
        ("F#5", 8, "る"), ("E5", 8, "よ"),
    ],
}
LYRICS = """\
夕焼け空に 光る印を
いつも探して 君を呼んでた
届かない声も 重ねた夢も
今日の風に 乗せていくよ

迷いながら それでも前に
震える手を 握りしめて
今こそ

届け 夕焼けシグナル 赤く燃える空へ
何度負けても 君がいるなら
届け 僕らのシグナル 夜が来る前に
この声枯れるまで 歌い続けるよ
"""


def vocal_line():
    """[(start_eighth, eighths, pitch, lyric)] for the whole song, rests dropped."""
    notes, t = [], START["verse"] * 8
    for sec in ("verse", "verse2", "pre", "chorus"):
        assert t == START[sec] * 8, (sec, t)
        for p, d, lyr in VOCAL[sec]:
            if p:
                notes.append((t, d, p, lyr))
            t += d
    return notes


# ---------------------------------------------------------------- MusicXML
def write_musicxml(path):
    """4/4, divisions = 2 per quarter (eighth = 1). Notes crossing a barline are tied."""
    steps = {0: ("C", 0), 1: ("C", 1), 2: ("D", 0), 3: ("D", 1), 4: ("E", 0), 5: ("F", 0),
             6: ("F", 1), 7: ("G", 0), 8: ("G", 1), 9: ("A", 0), 10: ("A", 1), 11: ("B", 0)}
    events, t = [], 0
    for start, dur, p, lyr in vocal_line():
        if start > t:
            events.append((t, start - t, None, None))
        events.append((start, dur, p, lyr))
        t = start + dur
    events.append((t, N_BARS * 8 - t, None, None))

    measures = [[] for _ in range(N_BARS)]
    for start, dur, p, lyr in events:
        first = True
        while dur > 0:
            bar, pos = divmod(start, 8)
            take = min(dur, 8 - pos)
            more = take < dur
            if p is None:
                measures[bar].append(f"<note><rest/><duration>{take}</duration></note>")
            else:
                step, alter = steps[midi(p) % 12]
                octave = midi(p) // 12 - 1
                pitch = f"<pitch><step>{step}</step>{'<alter>1</alter>' if alter else ''}<octave>{octave}</octave></pitch>"
                tie = ("" if first else '<tie type="stop"/>') + ('<tie type="start"/>' if more else "")
                tied = ("" if first else '<tied type="stop"/>') + ('<tied type="start"/>' if more else "")
                notations = f"<notations>{tied}</notations>" if tied else ""
                lyric = f"<lyric><text>{lyr}</text></lyric>" if first else ""
                measures[bar].append(f"<note>{pitch}<duration>{take}</duration>{tie}{notations}{lyric}</note>")
            start += take
            dur -= take
            first = False

    head = ('<attributes><divisions>2</divisions><key><fifths>4</fifths></key>'
            '<time><beats>4</beats><beat-type>4</beat-type></time><clef><sign>G</sign><line>2</line></clef></attributes>'
            f'<direction placement="above"><direction-type><metronome><beat-unit>quarter</beat-unit>'
            f'<per-minute>{BPM}</per-minute></metronome></direction-type><sound tempo="{BPM}"/></direction>')
    body = "".join(f'<measure number="{i + 1}">{head if i == 0 else ""}{"".join(m)}</measure>'
                   for i, m in enumerate(measures))
    xml = ('<?xml version="1.0" encoding="UTF-8"?><score-partwise version="3.1"><part-list>'
           '<score-part id="P1"><part-name>Vocal</part-name></score-part></part-list>'
           f'<part id="P1">{body}</part></score-partwise>')
    open(path, "w", encoding="utf-8").write(xml)


# ---------------------------------------------------------------- band
E8 = 60 / BPM / 2          # seconds per eighth
S16 = E8 / 2               # seconds per sixteenth


def note(inst, pitch, start16, len16, vel, jitter=0.004):
    t = start16 * S16 + random.uniform(-jitter, jitter)
    inst.notes.append(pretty_midi.Note(velocity=max(1, min(127, int(vel + random.randint(-6, 6)))),
                                       pitch=pitch, start=max(0, t), end=max(0, t) + len16 * S16 * 0.95))


def section_of(bar):
    for name, _ in reversed(SECTIONS):
        if bar >= START[name]:
            return name


def drums(pm):
    d = pretty_midi.Instrument(0, is_drum=True, name="drums")
    KICK, SNARE, HAT, OPEN, CRASH, RIDE, TOM_H, TOM_M, TOM_L = 36, 38, 42, 46, 49, 51, 50, 47, 45
    for bar in range(N_BARS):
        sec, b0 = section_of(bar), bar * 16
        last = bar + 1 == N_BARS or section_of(bar + 1) != sec
        if sec == "outro" and bar == N_BARS - 1:
            for p in (KICK, CRASH):
                note(d, p, b0, 8, 118)
            break
        if bar == START[sec] or (sec == "chorus" and bar == START[sec] + 8):
            note(d, CRASH, b0, 8, 110)
        if sec in ("intro", "chorus", "outro"):
            kicks, snares = (0, 4, 6, 8, 12), (4, 12)
            for s in range(2, 16, 4):
                note(d, OPEN, b0 + s, 2, 80)
            for s in range(0, 16, 2):
                note(d, HAT, b0 + s, 1, 62)
        elif sec == "pre":
            kicks, snares = (0, 10), (8,)
            for s in range(0, 16, 2):
                note(d, RIDE, b0 + s, 1, 74)
        else:
            kicks, snares = (0, 6, 8) + ((10,) if sec == "verse2" else ()), (4, 12)
            for s in range(0, 16, 2):
                note(d, HAT, b0 + s, 1, 70 if s % 4 == 0 else 56)
        fill = last and sec != "outro"
        for k in kicks:
            if not (fill and k >= 8):
                note(d, KICK, b0 + k, 1, 112)
        for s in snares:
            if not (fill and s >= 8):
                note(d, SNARE, b0 + s, 1, 108)
        if fill:                                  # sixteenth-note fill over the last two beats
            for i, p in enumerate([SNARE, SNARE, TOM_H, TOM_H, TOM_M, TOM_M, TOM_L, TOM_L]):
                note(d, p, b0 + 8 + i, 1, 88 + i * 4)
    pm.instruments.append(d)


def bass(pm):
    b = pretty_midi.Instrument(34, name="bass")    # Electric Bass (pick)
    for bar in range(N_BARS):
        sec = section_of(bar)
        for s0, s1, sym in chords_in_bar(bar):
            root, _ = chord_tones(sym)
            low = 28 + (root - 4) % 12             # E1 .. D#2
            for e in range(s0, s1):
                if sec == "outro" and bar == N_BARS - 1:
                    note(b, low, bar * 16, 8, 110)
                    break
                if sec == "pre":
                    pitch, vel = low, 96 if e % 2 == 0 else 80
                elif sec in ("chorus", "intro", "outro"):
                    pitch, vel = low + (12 if e % 2 else 0), 104
                else:
                    pitch, vel = low, 98
                note(b, pitch, bar * 16 + e * 2, 2, vel)
    pm.instruments.append(b)


def guitars(pm):
    """Two distorted rhythm guitars playing eighth-note power chords (panned apart in the mix)."""
    for name, prog, shift in (("gtrL", 30, 0), ("gtrR", 29, 0.012)):
        g = pretty_midi.Instrument(prog, name=name)
        for bar in range(N_BARS):
            sec = section_of(bar)
            if sec == "verse":
                continue                            # the first verse is guitar-free
            for s0, s1, sym in chords_in_bar(bar):
                root, _ = chord_tones(sym)
                r = 40 + (root - 4) % 12            # E2 ..
                shape = (r, r + 7, r + 12)
                if sec == "outro" and bar == N_BARS - 1:
                    for p in shape:
                        note(g, p, bar * 16, 16, 110)
                    break
                if sec == "pre":                    # let chords ring
                    for p in shape:
                        note(g, p, bar * 16 + s0 * 2, (s1 - s0) * 2, 84)
                    continue
                for e in range(s0, s1):
                    vel = 100 if sec != "verse2" else 82
                    length = 2 if sec != "verse2" else 1   # palm-muted in A'
                    for p in shape:
                        note(g, p, bar * 16 + e * 2, length, vel)
        for n in g.notes:
            n.start += shift
            n.end += shift
        pm.instruments.append(g)


def piano(pm):
    p = pretty_midi.Instrument(0, name="piano")
    for bar in range(N_BARS):
        sec = section_of(bar)
        for s0, s1, sym in chords_in_bar(bar):
            root, tones = chord_tones(sym)
            voicing = sorted({60 + (t - 60) % 12 for t in tones} | {72 + (tones[0] - 72) % 12})
            if sec in ("verse", "verse2", "pre"):   # sparkling eighth-note arpeggios
                seq = voicing + voicing[-2:0:-1]
                for i, e in enumerate(range(s0, s1)):
                    note(p, seq[i % len(seq)] + 12, bar * 16 + e * 2, 2, 70)
            elif sec == "outro" and bar == N_BARS - 1:
                for n_ in voicing:
                    note(p, n_, bar * 16, 16, 96)
            else:                                   # chorus / intro: syncopated stabs
                for e in (0, 3, 4, 6):
                    if s0 <= e < s1:
                        for n_ in voicing:
                            note(p, n_, bar * 16 + e * 2, 2, 84)
    pm.instruments.append(p)


def strings(pm):
    st = pretty_midi.Instrument(48, name="strings")
    for bar in range(N_BARS):
        if section_of(bar) not in ("pre", "chorus", "outro"):
            continue
        for s0, s1, sym in chords_in_bar(bar):
            root, tones = chord_tones(sym)
            for t in tones[:3]:
                note(st, 55 + (t - 55) % 12, bar * 16 + s0 * 2, (s1 - s0) * 2, 70, jitter=0)
            note(st, 67 + (tones[0] - 67) % 12, bar * 16 + s0 * 2, (s1 - s0) * 2, 64, jitter=0)
    pm.instruments.append(st)


def lead(pm):
    """The chorus hook on a saw lead, an octave up, in the intro and outro."""
    ld = pretty_midi.Instrument(81, name="lead")
    hook = [(t - START["chorus"] * 8, d, p) for t, d, p, _ in vocal_line()
            if START["chorus"] * 8 <= t < (START["chorus"] + 8) * 8]
    for base in (START["intro"] * 8, (START["outro"] + 2) * 8):
        for t, d, p in hook:
            if base + t + d > N_BARS * 8 - 8:
                continue
            note(ld, midi(p) + 12, (base + t) * 2, d * 2, 96, jitter=0)
    pm.instruments.append(ld)


def main():
    os.makedirs(OUT, exist_ok=True)
    assert len(BARS) == N_BARS
    for sec, notes in VOCAL.items():
        total = sum(d for _, d, _ in notes)
        assert total == len(dict(SECTIONS)[sec]) * 8 or sec == "chorus", (sec, total)
    write_musicxml(os.path.join(OUT, "vocal.musicxml"))
    for build in (drums, bass, guitars, piano, strings, lead):
        pm = pretty_midi.PrettyMIDI(initial_tempo=BPM)
        build(pm)
        for inst in pm.instruments:
            one = pretty_midi.PrettyMIDI(initial_tempo=BPM)
            one.instruments.append(inst)
            one.write(os.path.join(OUT, f"{inst.name}.mid"))
    open(os.path.join(OUT, "lyrics.txt"), "w", encoding="utf-8").write(LYRICS)
    print(f"{N_BARS} bars, {N_BARS * 8 * E8:.1f} s, {len(vocal_line())} sung notes")


if __name__ == "__main__":
    main()
