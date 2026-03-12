import re


def remove_whitespace_lines(txt: str) -> str:
    """Remove lines that contain only spaces"""

    txt = re.sub(r"^ +$", "", txt, flags=re.MULTILINE)
    return txt
