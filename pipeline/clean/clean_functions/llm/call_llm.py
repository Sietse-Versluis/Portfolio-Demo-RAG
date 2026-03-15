import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")


def call_llm(words: list[str]) -> list[str]:
    """Send a JSON array of words to the LLM. Returns a listS"""
    payload = json.dumps(words, ensure_ascii=False)

    response = requests.post(
        LM_STUDIO_URL,
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You receive a JSON array of Dutch words. "
                        "For each word: if it looks like two Dutch words merged without a space, "
                        "insert a single space at the correct position. "
                        "If the word is already correct, return it unchanged. "
                        "You may ONLY add one space per word — never change, remove, or add any letters. "
                        "Return a JSON array of exactly the same length. No explanation, only JSON."
                    ),
                },
                {"role": "user", "content": payload},
            ],
            "temperature": 0.0,
        },
    )

    raw = response.json()["choices"][0]["message"]["content"].strip()

    return raw
