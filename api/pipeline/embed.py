from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-base")


def embed(question: str) -> list[float]:
    """Embed a user question into a vector using the e5 multilingual model."""

    # intfloat/e5 models require "query: " prefix for questions
    vector = model.encode(f"query: {question}", normalize_embeddings=True)
    embedding = vector.tolist()
    return embedding
