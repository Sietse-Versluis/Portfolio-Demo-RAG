from extract import extract
from clean.clean import clean
from chunk.chunk import chunk


def run(pdf: str):
    txt = extract(pdf)
    txt = clean(txt)
    chunks = chunk(txt)


run("data/a55_manual.pdf")
