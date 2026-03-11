from extract import extract


def run(pdf: str):
    text = extract(pdf)
    print(text)


run("data/a55_manual.pdf")
