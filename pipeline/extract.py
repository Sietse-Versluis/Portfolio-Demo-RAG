from pathlib import Path
import pymupdf4llm


def extract(pdf: str) -> str:
    """Extracts text from a PDF and saves it as markdown, removing headers and footers to reduce noise."""

    # Skips header/footer
    md = pymupdf4llm.to_markdown(pdf, header=False, footer=False)

    # Export to output folder
    Path("output/extracted.md").write_text(md, encoding="utf-8")
    return md
