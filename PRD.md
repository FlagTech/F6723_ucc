# 簡易 Skill 系統

## 功能簡述

一個簡易的 skill 系統：

- skill 檔都放在工作資料夾下的 `skills/` 資料夾
- 每個 skill 就是單一的 `.md` 檔
- 每個 skill 檔都有 YAML front matter，記錄 `name`（技能名稱）與 `description`（功能簡述）

## 模組：`u_skills`

位於 `src/ucc/u_skills.py`。**載入模組時會自動呼叫 `load_skills()`。**

### `load_skills() -> None`

從 `skills/` 資料夾讀取所有 `.md` skill 檔，取得 front matter 資料，整理成以下格式並設定為 `get_skill` 的 docstring：

```
我是一個具備以下技能的函式：

- 技能名稱：技能簡述
- ...
```

行為細節：

- `skills/` 資料夾不存在時自動建立
- 資料夾內無 skill 檔時，docstring 設為「目前沒有任何技能。」
- front matter 無 `name` 欄位時，以檔案主幹名（stem）作為 fallback
- docstring 採用 Google 風格，動態部分（技能清單）之後附上靜態的 Args / Returns / Raises 區段

### `get_skill(skill_name: str) -> str`

根據提供的 skill 名稱（對應 front matter 的 `name` 欄位），傳回該 skill 檔 front matter 之後的完整 Markdown 內容。

找不到對應名稱時引發 `KeyError`。

## 測試

測試腳本位於 `tests/test_u_skills.py`，執行方式：

```bash
uv run tests/test_u_skills.py
```

腳本行為：

- 若 `skills/` 資料夾不存在，先建立
- 若 `skills/` 資料夾內沒有 skill 檔，先建立三個 skill 測試檔
- 測試 `load_skills()` 和 `get_skill()` 是否可以正確運作
