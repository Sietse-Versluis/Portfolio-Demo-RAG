import chromadb

client = chromadb.PersistentClient(path="output/chromadb")
collection = client.get_collection("a55_manual")


def vector_search(embedding: list[float], num_of_top_results: int) -> list[dict]:
    """Search ChromaDB for the top-N most similar chunks, returns chunk IDs and similarity scores."""

    results = collection.query(
        query_embeddings=[embedding], n_results=num_of_top_results
    )

    hits = []
    for id, distance in zip(results["ids"][0], results["distances"][0]):
        hits.append({"id": id, "score": round(1 - distance, 4)})

    return hits
