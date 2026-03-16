import re
import time
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

from .clean_functions.llm import call_llm


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


def fix_word_spacing(txt: str) -> str:
    lines = txt.splitlines()
    print(f"Total number of lines: {len(lines)}")

    for line_index, line in enumerate(lines):
        print(f"Line {line_index + 1} of {len(lines)}")

        words = line.split()

        if not words:
            print("Whitespace")
            continue

        # Only impacts temperatures
        time.sleep(2)

        for word_index, word in enumerate(words):
            if word.startswith("##"):
                continue
            if word in ["-", ",", ".", ":", ";"]:
                continue

            match = re.match(r"^(.*?)([.,;:!?]*)$", word)
            core = match.group(1)
            punctuation = match.group(2)

            fixed = call_llm(core, sentence=line)
            fixed = fixed.replace("_", " ") + punctuation
            print(f"{word} -> {fixed}")

            # Only impacts temperatures
            time.sleep(0.7)

            if fixed.replace(" ", "").lower() == word.lower():
                if word[0].isupper() and fixed[0].islower():
                    fixed = fixed[0].upper() + fixed[1:]
                words[word_index] = fixed

        lines[line_index] = " ".join(words)

    txt = "\n".join(lines)

    Path("output/cleaned_with_spacing.md").write_text(txt, encoding="utf-8")

    return txt
