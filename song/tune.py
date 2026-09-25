#!/usr/bin/env python3
"""Light pitch correction for out/vocal.wav -> out/vocal_tuned.wav.

Inside each sung note, the pitch is pulled toward the written note, keeping a
share of the natural movement (vibrato, scoops); the glides between notes are
left alone. Resynthesis uses WORLD, the same vocoder the NNSVS model uses.
"""
import os

import numpy as np
import pyworld as pw
import soundfile as sf

import compose as C

KEEP = 0.25           # share of the natural pitch deviation that survives
EDGE = 0.035          # seconds at each note edge left untouched (the glides)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

x, sr = sf.read(os.path.join(OUT, "vocal.wav"))
x = x.astype(np.float64)
fp = 5.0
f0, t = pw.harvest(x, sr, frame_period=fp, f0_floor=100, f0_ceil=1000)
sp = pw.cheaptrick(x, f0, t, sr)
ap = pw.d4c(x, f0, t, sr)

target = np.zeros_like(f0)
weight = np.zeros_like(f0)
for start, dur, p, _ in C.vocal_line():
    a, b = start * C.E8, (start + dur) * C.E8
    hz = 440 * 2 ** ((C.midi(p) - 69) / 12)
    idx = (t >= a) & (t < b)
    target[idx] = hz
    # full correction in the middle of the note, fading out toward its edges
    ramp = np.clip(np.minimum(t[idx] - a, b - t[idx]) / EDGE, 0, 1)
    weight[idx] = ramp

voiced = (f0 > 0) & (target > 0)
cents = np.zeros_like(f0)
cents[voiced] = 1200 * np.log2(f0[voiced] / target[voiced])
# a wildly off frame (octave slip) is snapped entirely; ordinary drift keeps KEEP of itself
cents = np.where(np.abs(cents) > 350, 0, cents)
tuned = f0.copy()
tuned[voiced] = target[voiced] * 2 ** (
    (cents[voiced] * (KEEP + (1 - KEEP) * (1 - weight[voiced]))) / 1200)

y = pw.synthesize(tuned, sp, ap, sr, fp)
y = y[: len(x)] / max(1e-9, np.abs(y).max()) * np.abs(x).max()
sf.write(os.path.join(OUT, "vocal_tuned.wav"), y.astype(np.float32), sr)
print("vocal_tuned.wav written")
