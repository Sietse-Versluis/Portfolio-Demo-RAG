import json

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

from .clean_functions.llm import call_llm, check_json


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
        print(f"line {line_index + 1} of {len(lines)}")

        words = line.split()

        if not words:
            continue

        original = []
        valid = []

        for index, word in enumerate(words):
            original.append((index, word))

        for index, word in enumerate(words):
            if word in ["-", ",", ".", ":", ";"]:
                continue
            if word.startswith("##"):
                continue
            valid.append((index, word))

        valid_indices = [index for index, _ in valid]
        valid_words = [word for _, word in valid]

        raw_results = call_llm(valid_words)

        if check_json(raw_results, len(valid_words)):
            results = json.loads(raw_results)
            print("LLM Result valid :)")
        else:
            results = valid_words
            print("LLM Result Invlid -> fallback to valid words")

        print("CHECKPOINT 1: Print Results")
        print(results)

        # Pair each result with its original position (from "valid") for later comparison
        results_indexed = list(zip(valid_indices, results))

        # Replace words in original with validated results where available
        results_dict = dict(results_indexed)

        final_words = []
        for index, word in original:
            if index in results_dict:
                result = results_dict[index]
                if result.replace(" ", "") == word:
                    final_words.append(result)
                else:
                    final_words.append(word)
            else:
                final_words.append(word)

        lines[line_index] = " ".join(final_words)

    txt = "\n".join(lines)

    Path("output/cleaned_fixed.md").write_text(txt, encoding="utf-8")

    return txt
