import re


def remove_italic(txt: str) -> str:
    """Strip *italic* and _italic_ markers"""

    txt = re.sub(
        r"(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)|(?<!_)_(?!_)(.*?)(?<!_)_(?!_)",
        r"\1\2",
        txt,
    )

    return txt
