import chromadb

client = chromadb.PersistentClient(path="output/chromadb")
collection = client.get_collection("a55_manual")


RELEVANCE_THRESHOLD = 0.65


def vector_search(embedding: list[float], top_k: int = 3) -> list[dict]:
    """Search ChromaDB for the most similar chunks.

    Returns up to `top_k` results with score >= RELEVANCE_THRESHOLD.
    Falls back to the single best result if none meet the threshold.
    """
    results = collection.query(query_embeddings=[embedding], n_results=top_k)

    hits = [
        {"id": id, "score": round(1 - distance, 4)}
        for id, distance in zip(results["ids"][0], results["distances"][0])
    ]

    relevant = [hit for hit in hits if hit["score"] >= RELEVANCE_THRESHOLD]

    if not relevant:
        return []

    return relevant
