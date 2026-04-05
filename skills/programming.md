---
name: 程式設計規範
description: 生成程式碼前一定要先讀過的程式設計規範
---
會協助開發程式，並遵守以下規範：

1. 先提出規劃，讓使用者同意後才將程式碼存檔

## Python 程式開發

一律使用 uv 管理 Python 環境：

1. 使用 `uv -h` 查使用說明
2. 禁止使用 pip

## 網頁設計

- 一律使用單一 HTML 檔設計，HTML、CSS、JavaScript 
    都寫在單一檔案內
- 不使用任何 JavaScript 框架。
- 測試時請用 python 建立本機伺服器以便自動化測試