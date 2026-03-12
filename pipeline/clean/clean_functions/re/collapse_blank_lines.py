import re


def collapse_blank_lines(txt: str) -> str:
    """Collapse 3+ consecutive newlines into 2"""

    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return txt
