# 夕焼けシグナル（vocal ver.）

動畫片頭曲風格的 J-pop，有歌聲、有樂團，約 80 秒（TV size）。作詞、作曲、編曲都寫在程式碼裡。

🎧 **[yuyake-signal.mp3](yuyake-signal.mp3)**

| 段落 | 小節 | 和聲 | 歌詞 |
|---|---|---|---|
| 前奏 | 8 | A–B–G#m–C#m–A–B–E | 合成器主奏副歌旋律 |
| A | 8 | C#m–A–B–E | 夕焼け空に 光る印を… |
| A' | 8 | C#m–A–B–G#m–A–F#m–B | 届かない声も 重ねた夢も… |
| B | 8 | 丸サ進行 AM7–G#7–C#m7–Bm7 E7 | 迷いながら それでも前に… 今こそ |
| サビ | 16 | 王道進行 IV–V–iii–vi | 届け 夕焼けシグナル… |
| 尾奏 | 8 | 回到前奏的旋律，E 和弦收尾 | |

E 大調、172 BPM。完整歌詞在 [lyrics.txt](lyrics.txt)。

## 怎麼做出來的

| 步驟 | 檔案 | 做什麼 |
|---|---|---|
| 1 | `compose.py` | 和弦、旋律＋歌詞、鼓／貝斯／雙吉他／鋼琴／弦樂／主奏的編曲 → `out/vocal.musicxml` 和每個樂器的 MIDI |
| 2 | `sing.py` | MusicXML → Sinsy 轉成音素標記 → [NNSVS](https://github.com/nnsvs/nnsvs) 神經網路歌聲合成 → `out/vocal.wav` |
| 3 | `tune.py` | 用 WORLD 聲碼器做輕度修音：音符中段拉到正確音高，保留 25% 的自然抖音，音與音之間的滑音不動 |
| 4 | `mix.py` | FluidSynth + FluidR3 GM 音色庫渲染樂器，pedalboard 做壓縮／EQ／回音／殘響、吉他左右聲道、副歌人聲加厚、段落動態，輸出 MP3 |

檢查過的數字：
- 旋律：強拍上沒有任何音落在和弦音上方半音（避開刺耳的音）
- 修音後 154 個音的音準中位誤差 4 音分，97% 在 50 音分內
- 人聲比伴奏大 1–2 dB（副歌約齊平），整體 -11 LUFS、峰值 -3 dBFS

## 重新產生

```sh
apt-get install fluidsynth fluid-soundfont-gm
python3 -m venv /opt/sing && . /opt/sing/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install "setuptools<70" h5py pyworld pysinsy nnsvs pedalboard pretty_midi pyloudnorm soundfile imageio-ffmpeg
# NNSVS 0.1.1 還沒跟上 NumPy 2 / 新版 SciPy，需要改兩行：
sed -i 's/L = int(fe.duration_features(p)\[0\])/L = int(np.asarray(fe.duration_features(p)).ravel()[0])/' $VIRTUAL_ENV/lib/python3*/site-packages/nnsvs/gen.py
sed -i 's/^    Wn = \[norm_cutoff\]$/    Wn = norm_cutoff/' $VIRTUAL_ENV/lib/python3*/site-packages/nnsvs/dsp.py
# 歌聲模型（NNSVS 預訓練模型 yoko）
curl -L -o yoko.tar.gz "https://www.dropbox.com/s/k8mya65yt52m0ps/yoko_latest.tar.gz?dl=1" && tar xzf yoko.tar.gz

python compose.py && NNSVS_MODEL=yoko_latest python sing.py && python tune.py && python mix.py
```

## 出處

- 詞・曲・編曲：Claude
- 歌聲：NNSVS（MIT）＋ r9y9 的預訓練模型 `yoko`；歌詞前處理用 Sinsy。模型的訓練語料與使用條款沒有公開說明，商業使用前請先確認。
- 樂器音色：FluidR3 GM soundfont（MIT）
