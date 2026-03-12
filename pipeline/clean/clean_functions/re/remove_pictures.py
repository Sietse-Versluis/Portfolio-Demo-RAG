import re


def remove_pictures(txt: str) -> str:
    """Remove picture markers like ==>...<== and **==>...<==**"""

    txt = re.sub(r"\*\*==>.*?<==\*\*|==>.*?<==", "", txt)
    return txt
