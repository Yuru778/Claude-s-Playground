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
| `git show ':/^frame 3000/'` | 直接看第 3000 幀 |
| `git log --reverse -p -- screen.txt` | 用 diff 播放，只顯示每一幀改變的列 |
| `git log --oneline \| wc -l` | 數數看總共幾幀 |
| GitHub 上 `screen.txt` 的 History | 每個 commit 的綠紅 diff 就是畫面變化 |

## 💬 網頁版：聊天視窗播 Bad Apple

`web/index.html` 是一個長得像 AI 聊天介面的網頁。一開始只是普通的聊天，但 AI 越講越怪，側邊欄也開始自己改名。故事的最後，頁面上的東西一個接一個被影子借走：

| 時間 | 誰在播 |
|---|---|
| 00:00 | 回覆裡的 code block |
| 00:27 | 一整面文字，每個字是一個像素 |
| 00:56 | 對話泡泡，分頁圖示也跟著播 |
| 01:31 | 建議按鈕 |
| 01:50 | 輸入框（ASCII） |
| 02:22 | 全部一起：側邊欄、訊息、按鈕、輸入框 |
| 03:23 | 謝幕，元素一個一個放手 |

- 線上版：<https://yuru778.github.io/Claude-s-Playground/>（`web/` 有變動就會由 GitHub Actions 自動部署）
- 也可以直接用瀏覽器打開 `web/index.html`，不需要伺服器
- **音樂**：故事中途可以選擇用 YouTube 播放（Alstroemeria Records 官方上傳的影繪版，嵌不了時改用轉載版），畫面會跟著播放器的時間走；也可以選自己的影片或音檔，或是不放音樂。倉庫裡不存放任何音訊
- 畫面和音樂對不上時，播放中按 `[` `]` 可以每次微調 0.05 秒
- 網址加上 `#play` 跳過故事，`#t=142` 從第 142 秒開始
- 每一段都切在 PV 的剪輯點上；按 `Esc` 停止
- 這是非官方的同人惡搞作品，與 Anthropic 無關

影格資料 `web/frames.js` 由 `python3 tools/build_web.py badapple.mp4` 產生：80×60 黑白、跟前一幀 XOR 後壓縮，約 560 KB。

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
