import chromadb


def safe_to_chromadb(embeddings: list[dict]):
    client = chromadb.PersistentClient(path="output/chromadb")

    try:
        client.delete_collection("a55_manual")
    except:
        pass

    collection = client.create_collection(name="a55_manual")

    ids = [embedding["id"] for embedding in embeddings]
    vectors = [embedding["embedding"] for embedding in embeddings]

    # ChromaDB links id/vector internaly by index from lists
    collection.add(
        ids=ids,
        embeddings=vectors,
    )

    print(f"ChromaDB: {collection.count()} chunks opgeslagen")
