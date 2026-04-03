"""簡易 Skill 系統模組。

提供從 skills/ 資料夾載入 Markdown skill 檔，並依名稱取得內容的功能。
"""

from pathlib import Path

_skill_registry: dict[str, Path] = {}

_GET_SKILL_STATIC_DOC = """
Args:
    skill_name: 要取得的 skill 名稱（對應 front matter 的 name 欄位）。

Returns:
    該 skill 的 Markdown 內容（front matter 之後的部分）。

Raises:
    KeyError: 若找不到對應名稱的 skill。
"""


def _parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """解析 Markdown 檔案的 YAML front matter。

    Args:
        text: 完整的 Markdown 檔案文字內容。

    Returns:
        (metadata_dict, body_text) 的 tuple。
        若格式不符，回傳 ({}, 原始文字)。
    """
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---", 4)
    if end == -1:
        return {}, text

    front = text[4:end]
    body = text[end + 4:].strip()

    metadata: dict[str, str] = {}
    for line in front.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            metadata[key.strip()] = value.strip()

    return metadata, body


def load_skills() -> None:
    """從 skills/ 資料夾載入所有 skill 並更新 get_skill 的 docstring。

    掃描工作目錄下的 skills/ 資料夾，讀取所有 .md 檔的 YAML front matter，
    建立 skill 名稱到檔案路徑的對映，並動態更新 get_skill.__doc__。
    若 skills/ 資料夾不存在，會自動建立。
    """
    skills_dir = Path.cwd() / "skills"
    skills_dir.mkdir(exist_ok=True)

    _skill_registry.clear()

    for path in skills_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        metadata, _ = _parse_front_matter(text)
        name = metadata.get("name", path.stem)
        _skill_registry[name] = path

    if _skill_registry:
        lines = []
        for name, path in sorted(_skill_registry.items()):
            text = path.read_text(encoding="utf-8")
            metadata, _ = _parse_front_matter(text)
            description = metadata.get("description", "")
            lines.append(f"- {name}：{description}")
        dynamic_part = "我是一個具備以下技能的函式：\n\n" + "\n".join(lines)
    else:
        dynamic_part = "目前沒有任何技能。"

    get_skill.__doc__ = dynamic_part + "\n" + _GET_SKILL_STATIC_DOC


def get_skill(skill_name: str) -> str:
    """（尚未載入 skills，請先呼叫 load_skills()）

    Args:
        skill_name: 要取得的 skill 名稱（對應 front matter 的 name 欄位）。

    Returns:
        該 skill 的 Markdown 內容（front matter 之後的部分）。

    Raises:
        KeyError: 若找不到對應名稱的 skill。
    """
    if skill_name not in _skill_registry:
        raise KeyError(f"Skill '{skill_name}' not found.")

    text = _skill_registry[skill_name].read_text(encoding="utf-8")
    _, body = _parse_front_matter(text)
    return body


load_skills()
