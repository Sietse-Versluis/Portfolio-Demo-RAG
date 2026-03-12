from pathlib import Path
from .clean_functions.re import (
    remove_pictures,
    remove_picture_text_blocks,
    remove_bold,
    remove_italic,
    remove_horizontal_rules,
    remove_br_tags,
    translate_md_table,
    remove_whitespace_lines,
    collapse_blank_lines,
    remove_arrow,
    merge_headers,
)


def clean(txt: str) -> str:
    txt = remove_pictures(txt)
    txt = remove_picture_text_blocks(txt)
    txt = remove_bold(txt)
    txt = remove_italic(txt)
    txt = remove_horizontal_rules(txt)
    txt = remove_br_tags(txt)
    txt = translate_md_table(txt)
    txt = remove_whitespace_lines(txt)
    txt = collapse_blank_lines(txt)
    txt = remove_arrow(txt)
    txt = merge_headers(txt)

    Path("output/cleaned.md").write_text(txt, encoding="utf-8")

    return txt


# voor llm

# als een functiewoord vastzit aan een
# inhoudswoord terwijl er een spatie hoort, fix het

# Cleaning stap:

# ✅ fix samengestelde woorden
