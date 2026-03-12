import json
from pathlib import Path
from extract import extract
from clean.clean import clean
from chunk.chunk import chunk
from clean.clean_functions.llm.local_llm import fix_word_spacing


def run(pdf: str):
    # 1-2: extract + clean
    cleaned_path = Path("output/cleaned.md")
    if cleaned_path.exists():
        txt = cleaned_path.read_text(encoding="utf-8")
    else:

        txt = extract(pdf)
        txt = clean(txt)

    # 3: chunk
    chunks_path = Path("output/chunks.json")
    if chunks_path.exists():
        chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    else:

        chunks = chunk(txt)

    # 4: LLM fix
    cleaned_chunks_path = Path("output/chunks_cleaned.json")
    if not cleaned_chunks_path.exists():

        fix_word_spacing(chunks)


run("data/a55_manual.pdf")
