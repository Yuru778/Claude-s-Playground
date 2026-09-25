#!/usr/bin/env python3
"""Sing out/vocal.musicxml with NNSVS: MusicXML -> Sinsy labels -> NNSVS -> out/vocal.wav.

    NNSVS_MODEL=/path/to/yoko_latest python3 sing.py
"""
import os
import sys

import numpy as np
import pysinsy
import soundfile as sf
from nnmnkwii.io import hts
from nnsvs.svs import SPSVS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
MODEL = os.environ.get("NNSVS_MODEL", "/opt/sing/models/yoko/yoko_latest")

sinsy = pysinsy.sinsy.Sinsy()
assert sinsy.setLanguages("j", pysinsy.get_default_dic_dir())
assert sinsy.loadScoreFromMusicXML(os.path.join(OUT, "vocal.musicxml"))
labels = hts.HTSLabelFile.create_from_contexts(sinsy.createLabelData(False, 1, 1).getData())
print(f"{len(labels)} phoneme labels", file=sys.stderr)
wav, sr = SPSVS(MODEL).svs(labels)
wav = wav.astype(np.float32) / 32768.0
sf.write(os.path.join(OUT, "vocal.wav"), wav, sr)
print(f"vocal.wav: {len(wav) / sr:.1f} s at {sr} Hz, peak {np.abs(wav).max():.2f}")
