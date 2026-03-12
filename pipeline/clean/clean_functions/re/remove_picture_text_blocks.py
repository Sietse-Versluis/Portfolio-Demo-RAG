import re


def remove_picture_text_blocks(txt: str) -> str:
    """Remove picture text blocks between --- Start/End of picture text --- markers"""

    txt = re.sub(
        r"\*\*-{5} Start of picture text -{5}\*\*.*?\*\*-{5} End of picture text -{5}\*\*",
        "",
        txt,
        flags=re.DOTALL,
    )

    return txt
