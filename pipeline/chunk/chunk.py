import json
import re
from pathlib import Path


def chunk(txt: str) -> list[dict]:
    """Splits cleaned markdown into chunks on ## headers, saves as JSON."""

    # Split on ## headers, keeping the header text
    sections = re.split(r"^## (.+)$", txt, flags=re.MULTILINE)

    chunks = []
    for chunk_id, section_index in enumerate(range(1, len(sections), 2)):
        title = sections[section_index].strip()
        content = sections[section_index + 1].strip()
        chunks.append({"id": chunk_id, "title": title, "content": content})

    Path("output/chunks.json").write_text(
        json.dumps(chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return chunks
