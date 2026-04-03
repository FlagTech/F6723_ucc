"""u_skills 模組的測試腳本。

測試流程：
1. 建立 skills/ 資料夾（若不存在）
2. 建立三個測試 skill 檔（若資料夾內無 .md 檔）
3. 測試 load_skills() 和 get_skill() 的正確性
"""

from pathlib import Path

from ucc.u_skills import get_skill, load_skills

SKILLS_DIR = Path.cwd() / "skills"

TEST_SKILLS = [
    {
        "file": "python-basics.md",
        "name": "Python 基礎",
        "description": "提供 Python 基本語法與資料型別的說明",
        "body": "# Python 基礎\n\n本 skill 涵蓋變數、迴圈、函式等基礎概念。\n",
    },
    {
        "file": "file-operations.md",
        "name": "檔案操作",
        "description": "讀取與寫入本地檔案的方法",
        "body": "# 檔案操作\n\n使用 pathlib 和 open() 處理檔案。\n",
    },
    {
        "file": "api-design.md",
        "name": "API 設計",
        "description": "RESTful API 的設計原則與最佳實務",
        "body": "# API 設計\n\n包含路由設計、狀態碼使用與版本控制。\n",
    },
]


def setup_test_environment() -> None:
    """建立 skills/ 資料夾與測試 skill 檔（若尚未存在）。"""
    SKILLS_DIR.mkdir(exist_ok=True)

    if not list(SKILLS_DIR.glob("*.md")):
        for skill in TEST_SKILLS:
            content = (
                f"---\n"
                f"name: {skill['name']}\n"
                f"description: {skill['description']}\n"
                f"---\n"
                f"{skill['body']}"
            )
            (SKILLS_DIR / skill["file"]).write_text(content, encoding="utf-8")
        print(f"已建立 {len(TEST_SKILLS)} 個測試 skill 檔於 {SKILLS_DIR}")


def test_load_skills() -> None:
    """測試 load_skills() 能正確更新 get_skill 的 docstring。"""
    load_skills()

    doc = get_skill.__doc__
    assert doc is not None, "get_skill.__doc__ 不應為 None"
    assert "我是一個具備以下技能的函式：" in doc, "docstring 應包含技能清單標題"
    assert "Python 基礎" in doc, "docstring 應包含 'Python 基礎'"
    assert "檔案操作" in doc, "docstring 應包含 '檔案操作'"
    assert "API 設計" in doc, "docstring 應包含 'API 設計'"

    print("=== get_skill.__doc__ ===")
    print(doc)
    print("========================")
    print("test_load_skills 通過")


def test_get_skill() -> None:
    """測試 get_skill() 能正確傳回 skill 內容。"""
    content = get_skill("Python 基礎")
    assert "# Python 基礎" in content, "body 應包含標題"
    assert "變數" in content, "body 應包含預期內容"
    assert "name:" not in content, "body 不應包含 front matter"
    assert "description:" not in content, "body 不應包含 front matter"

    print("=== get_skill('Python 基礎') ===")
    print(content)
    print("================================")

    try:
        get_skill("不存在的技能")
        assert False, "應引發 KeyError"
    except KeyError:
        pass

    print("test_get_skill 通過")


def main() -> None:
    setup_test_environment()
    test_load_skills()
    test_get_skill()
    print("\n所有測試通過")


if __name__ == "__main__":
    main()
