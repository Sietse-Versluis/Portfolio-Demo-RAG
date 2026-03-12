import re


def remove_br_tags(txt: str) -> str:
    """Replace <br> tags with a space"""

    txt = re.sub(r"<br\s*/?>", " ", txt)
    return txt
