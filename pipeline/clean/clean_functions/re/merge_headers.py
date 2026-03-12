import re


def merge_headers(txt: str) -> str:
    """Merge headers without content and leaves only one time ##"""

    merge = re.compile(r"^(#{1,6} .+?)[ \t]*\n+(#{1,6}) (.+)", re.MULTILINE)
    while merge.search(txt):
        txt = merge.sub(r"\1 — \3", txt)

    return txt
