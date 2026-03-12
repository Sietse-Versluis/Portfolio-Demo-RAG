from extract import extract
from clean.clean import clean


def run(pdf: str):
    txt = extract(pdf)
    txt = clean(txt)


run("data/a55_manual.pdf")
