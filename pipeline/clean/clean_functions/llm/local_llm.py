import json
import os
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")


def fix_word_spacing(chunks: list[dict]) -> list[dict]:
    """Sends each chunk to the LLM to fix missing spaces between words. Fresh context per chunk."""

    cleaned = []

    total = len(chunks)

    for chunk in chunks:
        print(f"fix_word_spacing llm: chunk {chunk['id']} of {total}")
        response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": "local-model",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a Dutch text editor. "
                            "Fix only concatenated words where a space is missing "
                            "(e.g. 'voorhet' → 'voor het', 'batterijop' → 'batterij op'). "
                            "Change NOTHING else. Return only the corrected text, no explanations."
                        ),
                    },
                    {
                        "role": "user",
                        "content": chunk["content"],
                    },
                ],
                "temperature": 0.0,
            },
        )

        cleaned_content = response.json()["choices"][0]["message"]["content"]

        cleaned.append(
            {
                "id": chunk["id"],
                "title": chunk["title"],
                "content": cleaned_content,
            }
        )

    Path("output/chunks_cleaned.json").write_text(
        json.dumps(cleaned, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return cleaned
