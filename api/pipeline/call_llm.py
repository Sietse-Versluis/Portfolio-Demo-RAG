import os

import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")


def call_llm(question: str, chunks: list[dict]) -> str:
    """Send a question and retrieved chunks to the LLM, returns the answer as a string."""

    context = "\n\n".join(f"{chunk['title']}:\n{chunk['content']}" for chunk in chunks)

    response = requests.post(
        LM_STUDIO_URL,
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Je bent een behulpzame assistent voor de Samsung Galaxy handleiding. "
                        "Beantwoord de vraag uitsluitend op basis van de onderstaande context. "
                        "Als het antwoord niet in de context staat, zeg dan dat je het niet weet. "
                        "Antwoord altijd in het Nederlands. Wees beknopt en duidelijk."
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
