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

`web/index.html` 是一個長得像 AI 聊天介面的網頁。打開是模仿的聊天頁面，先跳出一個同樣風格的語言提示（17 種語言，標題用多國文字的亂碼在各語言之間切換），接著是普通的聊天，但 AI 越講越怪，側邊欄也開始自己改名。它想坦白些什麼，講到一半開始故障：口吃、亂碼、回覆斷掉，最後跳出錯誤和「要自動修復 Claude 嗎？」的視窗（附閃光警告，「取消」會變成「修復」）。按下修復之後，頁面上的東西一個接一個被影子借走：

| 時間 | 誰在播 |
|---|---|
| 00:00 | 回覆裡的 code block |
| 00:27 | 一整面文字，每個字是一個像素 |
| 00:56 | 對話泡泡，分頁圖示也跟著播 |
| 01:31 | 建議按鈕 |
| 01:50 | 輸入框（ASCII） |
| 02:22 | 關燈：切成 dark mode，每個字和按鈕都是像素，亮起的地方就是 PV 的白色（側邊欄和對話標題是文字本身發白光）；每次換場，版面會被甩開、切碎再彈回來 |
| 03:00 | 版面？不需要了：整個介面飛散，換成滿版的 UI 零件，依畫面亮度縮放 |
| 03:23 | 謝幕：零件一個個掉下去，最後是謝幕畫面，可以重新播放或回到最開始 |

按下「修復」後會先用遮罩蓋住頁面、箭頭指向播放器，讓你把 YouTube 的廣告略過（如果有的話），準備好再開始。

- 線上版：<https://yuru778.github.io/Claude-s-Playground/>（`web/` 有變動就會由 GitHub Actions 自動部署）
- 也可以直接用瀏覽器打開 `web/index.html`，不需要伺服器
- **音樂**：不會詢問，YouTube 播放器在聊天時悄悄載入，演出開始才出現。優先用與影格時間軸相同的 NicoNico 原版 PV 轉載（03:39），嵌不了才改用 Alstroemeria Records 官方版（03:53，拍子可能對不上）。畫面會跟著播放器的時間走；倉庫裡不存放任何音訊
- 畫面和音樂對不上時，播放中按 `[` `]` 可以每次微調 0.05 秒
- 網址加上 `?lang=ja` 跳過語言提示，`#play` 跳過故事，`#t=142` 從第 142 秒開始
- 每一段都切在 PV 的剪輯點上；按 `Esc` 停止
- 這是非官方的同人惡搞作品，與 Anthropic 無關

影格資料 `web/frames.js` 由 `python3 tools/build_web.py badapple.mp4` 產生：80×60 黑白、跟前一幀 XOR 後壓縮，約 560 KB。

文字都在 `tools/i18n/*.json`（以 `en.json` 為準），改完執行 `python3 tools/build_i18n.py` 重新產生 `web/i18n.js`，它會檢查每個語言的欄位、陣列長度和 `{placeholder}` 是否一致。

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

## 🎵 夕焼けシグナル（Sunset Signal）：用 Strudel 寫的 J-pop

[`web/music/yuyake-signal.js`](web/music/yuyake-signal.js) 是一首用 [Strudel](https://strudel.cc) 程式碼寫成的 J-pop 器樂曲，原創旋律，約 1 分鐘。

▶ **直接聽：<https://yuru778.github.io/Claude-s-Playground/sunset.html>**（會自動打開 strudel.cc 並載入程式碼，按播放或 Ctrl+Enter）

| 段落 | 小節 | 和聲 |
|---|---|---|
| 前奏 | 4 | 王道進行前半，琶音＋鋪底，最後一小節小鼓滾奏 |
| A 段 | 8 | Bm–G–A–D，鋼琴切分、8 分音符貝斯 |
| B 段 | 8 | 丸サ進行 GM7–F#7–Bm7–Am7 D7，最後停在 A 準備進副歌 |
| 副歌 | 8 | 王道進行 IV–V–iii–vi（G–A–F#m–Bm–Em–A–D） |
| 間奏 | 2 | A → B♭，爵士鼓過門，旋律往上爬 |
| 最後副歌 | 8 | 整首升半音到 E♭（J-pop 經典的最後轉調） |
| 尾奏 | 4 | A♭–B♭–E♭ 收尾 |

- 速度 172 BPM（`setcpm(172 / 4)`，一個 cycle 一小節），D 大調
- 音色：supersaw 主旋律、鋼琴、supersaw 鋪底、三角波琶音、鋸齒波貝斯、TR-909 鼓組
- 寫好後用 `@strudel/core` 在 Node 裡實際執行、逐小節檢查過：112 個強拍旋律音沒有任何一個落在和弦音上方半音
