import re


def remove_arrow(txt: str) -> str:
    """Remove arrow/triangle characters"""

    txt = re.sub(r"▶\s*", "", txt)
    return txt
