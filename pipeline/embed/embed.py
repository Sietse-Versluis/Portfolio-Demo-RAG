import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-base")


def embed(chunks: list[dict]) -> list[dict]:
    # intfloat/e5 models require "passage: " the chunk (title + content)
    chunk_texts = []
    for chunk in chunks:
        txt = f"passage: {chunk['title']}\n{chunk['content']}"
        chunk_texts.append(txt)

        print(txt)

    chunk_vectors = model.encode(
        chunk_texts, show_progress_bar=True, normalize_embeddings=True
    )

    embedded_chunks = []
    for chunk, vector in zip(chunks, chunk_vectors):
        embedded_chunks.append(
            {
                "id": str(chunk["id"]),
                "embedding": vector.tolist(),
            }
        )

    Path("output/embeddings.json").write_text(
        json.dumps(embedded_chunks, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return embedded_chunks
