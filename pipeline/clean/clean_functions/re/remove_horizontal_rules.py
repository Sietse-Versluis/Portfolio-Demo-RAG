import re


def remove_horizontal_rules(txt: str) -> str:
    """Remove horizontal lines (---, ***, ___, - - -, * * *)"""

    txt = re.sub(
        r"^(\-{3,}|\*{3,}|_{3,}|-\s-\s-|\*\s\*\s\*)$", "", txt, flags=re.MULTILINE
    )

    return txt
