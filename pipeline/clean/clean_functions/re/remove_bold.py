import re


def remove_bold(txt: str) -> str:
    """Strip **bold** and __bold__ markers"""

    txt = re.sub(r"\*\*(.*?)\*\*|__(.*?)__", r"\1\2", txt)
    return txt
