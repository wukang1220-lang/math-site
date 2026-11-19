# 數學方格簿

國中數學七、八、九年級學習網站（108 課綱，對照翰林、康軒、南一章節順序）。

- 網站：https://wukang1220-lang.github.io/math-site/
- 6 冊、24 章、60 個單元；每個單元有重點整理（關鍵詞紅字）、圖解或互動工具、例題，以及 15 題的練習題庫（每次隨機抽 8 題、選項順序隨機，答對灑花，8 題全對灑大花）。
- 每個單元標出 106–115 年國中教育會考的出題數與題號。
- 文字、例題、練習題皆為自編；教材與題庫只用來確認範圍。

## 檔案

| 路徑 | 內容 |
|---|---|
| `structure.json` | 冊、章、節與會考資料（由 `make_structure.py` 從 `data/capmap.json` 產生） |
| `content/b1.txt` … `b6.txt` | 各冊重點、例題與原有題目 |
| `content/q1.txt` … `q6.txt` | 各冊新增題目（`@+ 單元` 接續原單元） |
| `art/figs/*.svg` | 幾何圖解；`python -I art/check_svg.py figs` 檢查 |
| `tpl.html` | 頁面模板（版面、練習、互動工具） |
| `build.py` | 產生 `docs/index.html`（GitHub Pages）與上一層的 `math-site.html` |

## 建置

```
python -I build.py --check   # 只檢查內容
python -I build.py           # 產生網站
```

題目只能往後新增、不要調整既有順序（答題紀錄用「單元.題號」記錄）。
