#!/usr/bin/env python3
"""Render the band with FluidSynth and mix it with the vocal -> yuyake-signal.mp3

    python3 compose.py && python3 sing.py && python3 tune.py && python3 mix.py

Needs fluidsynth with a General MIDI soundfont (FluidR3_GM), ffmpeg (or
imageio-ffmpeg), pedalboard, pyloudnorm and soundfile.
"""
import os
import shutil
import subprocess

import numpy as np
import pedalboard as pb
import pyloudnorm
import soundfile as sf

import compose as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SF2 = os.environ.get("SOUNDFONT", "/usr/share/sounds/sf2/FluidR3_GM.sf2")
SR = 48000
DOTTED_EIGHTH = 0.75 * 60 / C.BPM

# stem: (target RMS dBFS while playing, pan -1..1 or None to keep the soundfont's stereo, effects)
STEMS = {
    "drums":   (-19, None, [pb.Compressor(threshold_db=-16, ratio=3, attack_ms=3, release_ms=90)]),
    "bass":    (-21, 0.0,  [pb.Compressor(threshold_db=-20, ratio=4, attack_ms=5, release_ms=120),
                            pb.LowpassFilter(cutoff_frequency_hz=3500)]),
    "gtrL":    (-25, -0.8, [pb.HighpassFilter(110), pb.Distortion(drive_db=8), pb.LowpassFilter(7500),
                            pb.Compressor(threshold_db=-20, ratio=3)]),
    "gtrR":    (-25, 0.8,  [pb.HighpassFilter(110), pb.Distortion(drive_db=8), pb.LowpassFilter(7500),
                            pb.Compressor(threshold_db=-20, ratio=3)]),
    "piano":   (-27, 0.25, [pb.HighpassFilter(200), pb.Reverb(room_size=0.5, wet_level=0.2, dry_level=0.9)]),
    "strings": (-28, -0.2, [pb.Reverb(room_size=0.7, wet_level=0.3, dry_level=0.8)]),
    "lead":    (-22, 0.0,  [pb.Delay(delay_seconds=DOTTED_EIGHTH, feedback=0.3, mix=0.2),
                            pb.Reverb(room_size=0.5, wet_level=0.2, dry_level=0.9)]),
}
VOCAL_DB = -17
VOCAL_FX = [
    pb.HighpassFilter(120),
    pb.Compressor(threshold_db=-22, ratio=4, attack_ms=4, release_ms=80),
    pb.PeakFilter(cutoff_frequency_hz=3000, gain_db=3, q=0.8),
    pb.HighShelfFilter(cutoff_frequency_hz=9000, gain_db=2),
    pb.Delay(delay_seconds=DOTTED_EIGHTH, feedback=0.22, mix=0.1),
    pb.Reverb(room_size=0.45, damping=0.5, wet_level=0.16, dry_level=1.0),
]
SECTION_DB = {"verse": -3.5, "verse2": -2.5, "pre": -1.5}
TARGET_LUFS = -11
MASTER = [
    pb.Compressor(threshold_db=-12, ratio=2, attack_ms=20, release_ms=150),
    pb.Limiter(threshold_db=-1.5, release_ms=80),
]


def render(stem):
    wav = os.path.join(OUT, f"{stem}.wav")
    subprocess.run(["fluidsynth", "-ni", "-g", "0.7", "-r", str(SR), "-R", "0", "-C", "0",
                    "-F", wav, SF2, os.path.join(OUT, f"{stem}.mid")],
                   check=True, capture_output=True)
    x, sr = sf.read(wav, always_2d=True)
    assert sr == SR
    return x.T.astype(np.float32)             # (2, n)


def active_rms_db(x):
    mono = x.mean(axis=0)
    frames = mono[: len(mono) // 2400 * 2400].reshape(-1, 2400)
    rms = np.sqrt((frames ** 2).mean(axis=1))
    loud = rms[rms > rms.max() * 0.05]
    return 20 * np.log10(np.sqrt((loud ** 2).mean()) + 1e-12)


def fit(x, n):
    return np.pad(x, ((0, 0), (0, max(0, n - x.shape[1]))))[:, :n]


def pan(x, p):
    mono = x.mean(axis=0)
    left, right = np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)
    return np.stack([mono * left, mono * right]) * np.sqrt(2)


def main():
    n = int((C.N_BARS * 8 * C.E8 + 2.5) * SR)   # song plus a reverb tail
    mix = np.zeros((2, n), np.float32)
    for stem, (target, p, fx) in STEMS.items():
        x = fit(render(stem), n)
        if p is not None:
            x = pan(x, p)
        x = pb.Pedalboard(fx)(x, SR)
        x *= 10 ** ((target - active_rms_db(x)) / 20)
        mix += x

    # dynamics: the band holds back in the verses and opens up in the chorus
    env = np.ones(n, np.float32)
    for name, sec in C.SECTIONS:
        a = int(C.START[name] * 8 * C.E8 * SR)
        env[a:] = 10 ** (SECTION_DB.get(name, 0) / 20)
    ramp = int(0.08 * SR)
    env = np.convolve(env, np.ones(ramp) / ramp, mode="same").astype(np.float32)
    mix *= env
    band = mix.copy()

    v, sr = sf.read(os.path.join(OUT, "vocal_tuned.wav"))
    assert sr == SR
    v = np.stack([v, v]).astype(np.float32)
    v = fit(v, n)
    v = pb.Pedalboard(VOCAL_FX)(v, SR)
    v *= 10 ** ((VOCAL_DB - active_rms_db(v)) / 20)
    c0 = int(C.START["chorus"] * 8 * C.E8 * SR)
    v[:, c0:] *= 10 ** (2 / 20)              # the chorus vocal rides over the full band
    # chorus: two short delayed copies spread left and right thicken the voice
    c0, c1 = int(C.START["chorus"] * 8 * C.E8 * SR), int((C.START["chorus"] + 17) * 8 * C.E8 * SR)
    for delay_ms, side in ((17, -0.7), (26, 0.7)):
        d = int(delay_ms / 1000 * SR)
        dbl = np.zeros_like(v)
        dbl[:, c0 + d:c1] = v[:, c0:c1 - d]
        mix += pan(dbl, side) * 10 ** (-9 / 20)
    mix += v
    for name, sec in C.SECTIONS:
        a = int(C.START[name] * 8 * C.E8 * SR)
        z = int((C.START[name] + len(sec)) * 8 * C.E8 * SR)
        if np.abs(v[:, a:z]).max() > 0.01:
            print(f"  {name:7} vocal {active_rms_db(v[:, a:z]) - active_rms_db(band[:, a:z]):+5.1f} dB over the band")

    # pedalboard's Limiter adds make-up gain, so it goes first and a plain gain sets the level last:
    # J-pop-ish loudness, but never letting peaks above -1 dBFS
    mix = pb.Pedalboard(MASTER)(mix, SR)
    meter = pyloudnorm.Meter(SR)
    gain_db = min(TARGET_LUFS - meter.integrated_loudness(mix.T), -1 - 20 * np.log10(np.abs(mix).max()))
    mix *= 10 ** (gain_db / 20)
    fade = int(1.5 * SR)
    mix[:, -fade:] *= np.linspace(1, 0, fade)

    wav = os.path.join(OUT, "mix.wav")
    sf.write(wav, mix.T, SR)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        import imageio_ffmpeg
        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    mp3 = os.path.join(HERE, "yuyake-signal.mp3")
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "256k",
                    "-metadata", "title=夕焼けシグナル", "-metadata", "artist=Claude (vocal: NNSVS yoko)", mp3], check=True)
    print(f"{mp3}: {mix.shape[1] / SR:.1f} s, {meter.integrated_loudness(mix.T):.1f} LUFS, "
          f"peak {20 * np.log10(np.abs(mix).max()):.1f} dBFS")


if __name__ == "__main__":
    main()
