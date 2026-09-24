# 🍎 Bad Apple!! on Git

這個倉庫**本身**就是 Bad Apple!!。

- **6573 個 commit，每個 commit 是一幀**（30 fps，3 分 39 秒）
- 每一幀是 80×30 的文字畫面，用 `█ ▀ ▄` 半格方塊畫出 80×60 的黑白像素
- 同一幀存在兩個地方：**commit 訊息的內文**，以及 tree 裡的 **`screen.txt`**
- 播放器 `play.sh` 只做一件事：以 30 fps 把 `git log` 串流到終端機

## ▶ 播放

```sh
git clone https://github.com/Yuru778/Claude-s-Playground.git
cd Claude-s-Playground
./play.sh
```

- 終端機至少要 80×31
- `FPS=15 ./play.sh` 慢動作，`Ctrl+C` 停止
- 倉庫裡沒有聲音，可以另外打開原版 PV，和 `./play.sh` 同時開始播

## 用其他方式看

| 指令 | 會看到什麼 |
|---|---|
| `git log --reverse` | 用分頁器一格一格翻 |
| `git show HEAD~3000:screen.txt` | 任意一幀（`HEAD` 是最後一幀） |
| `git log --reverse -p -- screen.txt` | 用 diff 播放，只顯示每一幀改變的列 |
| `git log --oneline \| wc -l` | 數數看總共幾幀 |
| GitHub 上 `screen.txt` 的 History | 每個 commit 的綠紅 diff 就是畫面變化 |

## 🔧 自己重新產生

```sh
pip install numpy imageio-ffmpeg     # 或是系統裝了 ffmpeg 也可以
python3 tools/build.py badapple.mp4 | git fast-import
```

`tools/build.py` 會把影片縮成 80×60、轉成黑白，接到目前分支後面，每幀一個 commit，時間戳記每幀相差一秒。

## 出處

- 原曲：ZUN《東方幻想郷 〜 Lotus Land Story》〈Bad Apple!!〉
- 編曲：Alstroemeria Records《Bad Apple!! feat. nomico》
- 影繪 PV：あにら（NicoNico `sm8628149`）

這個倉庫只存 80×60 的黑白剪影，不包含影片或音訊。
