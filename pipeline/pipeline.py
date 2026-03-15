from pathlib import Path
from extract import extract
from clean.clean import clean, fix_word_spacing
from chunk.chunk import chunk


def run(pdf: str):
    # 1-2: extract + clean (regex)
    cleaned_path = Path("output/cleaned.md")
    if cleaned_path.exists():
        txt = cleaned_path.read_text(encoding="utf-8")
    else:
        txt = extract(pdf)
        txt = clean(txt)

    fix_word_spacing(txt)


run("data/a55_manual.pdf")
