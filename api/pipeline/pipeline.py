from api.pipeline.call_llm import call_llm
from api.pipeline.embed import embed
from api.pipeline.retrieve_chunks import retrieve_chunks
from api.pipeline.vector_search import vector_search


async def pipeline(question: str) -> dict:
    embedding = embed(question)
    hits = vector_search(embedding, 3)
    chunks = retrieve_chunks(hits)
    answer = call_llm(question, chunks)

    return {
        "answer": answer,
        "sources": [
            {
                "id": chunk["id"],
                "title": chunk["title"],
                "score": chunk["score"],
                "content": chunk["content"],
            }
            for chunk in chunks
        ],
    }
