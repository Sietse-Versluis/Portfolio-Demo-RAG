from api.pipeline.embed import embed
from api.pipeline.vector_search import vector_search


async def pipeline(question: str) -> dict:
    embedding = embed(question)
    hits = vector_search(embedding, 3)
    print(hits)
    return {question}
