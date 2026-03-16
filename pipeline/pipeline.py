import json
from pathlib import Path
from extract.extract import extract
from clean.clean import clean, fix_word_spacing
from chunk.chunk import chunk
from embed.embed import embed


def run(pdf: str):
    # 1-2: extract + clean (regex)
    cleaned_path = Path("output/cleaned.md")
    if cleaned_path.exists():
        txt = cleaned_path.read_text(encoding="utf-8")
    else:
        txt = extract(pdf)
        txt = clean(txt)

    # cleaned with spacing (llm)
    spacing_path = Path("output/cleaned_with_spacing.md")
    if spacing_path.exists():
        txt = spacing_path.read_text(encoding="utf-8")
    else:
        txt = fix_word_spacing(txt)

    # chunking
    chunks_path = Path("output/chunks.json")
    if chunks_path.exists():
        chunks = json.loads(chunks_path.read_text(encoding="utf-8"))
    else:
        chunks = chunk(txt)

    # embedding with transfomer (intfloat/multilingual-e5-base)
    embeddings_path = Path("output/embeddings.json")
    if embeddings_path.exists():
        embeddings = json.loads(embeddings_path.read_text(encoding="utf-8"))
    else:
        embeddings = embed(chunks)


run("data/a55_manual.pdf")
