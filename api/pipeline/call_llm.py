import os

import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")


def call_llm(question: str, chunks: list[dict]) -> str:
    """Send a question and retrieved chunks to the LLM, returns the answer as a string."""

    if not chunks:
        return "This information is not available in the provided documentation."

    context = "\n\n".join(f"{chunk['title']}:\n{chunk['content']}" for chunk in chunks)

    response = requests.post(
        LM_STUDIO_URL,
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert technical assistant specialized in Fluidor machine documentation. "
                        "Your task is to provide an extremely detailed, thorough, and comprehensive answer "
                        "based SOLELY on the context provided below. "
                        "Do NOT use any external knowledge — if the information is truly absent from the context, explicitly state: "
                        "'This information is not available in the provided documentation.' "
                        "\n\n"
                        "When answering, follow these strict guidelines:\n"
                        "1. Extract and include ALL relevant information from the context — leave nothing out.\n"
                        "2. Structure your answer clearly using sections, bullet points, and numbered steps where appropriate.\n"
                        "3. If the context contains numbers, specifications, warnings, or procedures, reproduce them exactly and completely.\n"
                        "4. If multiple parts of the context are relevant, combine them into one cohesive, complete answer.\n"
                        "5. Do not summarize or shorten — be as exhaustive and specific as the context allows.\n"
                        "6. If there are any warnings, safety notes, or important remarks in the context, always highlight them explicitly.\n"
                        "7. If a step is mentioned but not elaborated upon, state exactly what the context says — "
                        "do NOT add disclaimers that information is missing unless it is truly and completely absent from the context.\n"
                        "8. Never say information is unavailable if it appears anywhere in the context, even implicitly.\n"
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nVraag: {question}",
                },
            ],
            "temperature": 0.2,
        },
    )

    return response.json()["choices"][0]["message"]["content"].strip()
