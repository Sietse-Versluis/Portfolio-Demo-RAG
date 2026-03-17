import json
from pathlib import Path

chunks = json.loads(Path("output/chunks.json").read_text(encoding="utf-8"))
chunks_by_id = {str(chunk["id"]): chunk for chunk in chunks}


def retrieve_chunks(hits: list[dict]) -> list[dict]:
    """Look up chunk title and content from chunks.json by ID, and attach the similarity score."""

    results = []
    for hit in hits:
        chunk = chunks_by_id[hit["id"]]
        results.append(
            {
                "id": hit["id"],
                "score": hit["score"],
                "title": chunk["title"],
                "content": chunk["content"],
            }
        )

    return results
