import os

import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")


def call_llm(word: str, sentence: str = "") -> str:
    """Send a single Dutch word to the LLM, with optional sentence context. Returns the word, with a space inserted if two words were merged."""
    context_line = f'\n\nContext sentence: "{sentence}"' if sentence else ""

    response = requests.post(
        LM_STUDIO_URL,
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You receive a single Dutch word and optionally the sentence it appears in. "
                        "If the word looks like two or more separate words merged without spaces (an OCR error), insert spaces at the correct positions. "
                        "Use the sentence context only to understand the topic — the context sentence itself may also contain OCR merge errors, so do not treat it as correct Dutch. "
                        "Valid Dutch compound words (like 'pincode', 'wachtwoord', 'voorzorgsmaatregelen', 'gezichtsherkenning') must NOT be split. "
                        "Short words like 'uw', 'de', 'in', 'om', 'op' are always valid and must NOT be split. "
                        "You may ONLY add spaces — never change, remove, or add any letters. "
                        "Do not add spaces before or after the word. "
                        "Return ONLY the (corrected) word, no explanation, no punctuation, nothing else.\n\n"
                        "Examples:\n"
                        "voorhet -> voor het\n"
                        "wanneeru -> wanneer u\n"
                        "dooriemand -> door iemand\n"
                        "minderveilig -> minder veilig\n"
                        "ervoordat -> ervoor dat\n"
                        "apparaat -> apparaat\n"
                        "uw -> uw\n"
                        "pincode -> pincode\n"
                        "wachtwoord -> wachtwoord\n"
                        "gezichtsherkenning -> gezichtsherkenning\n"
                        "schermvergrendeling -> schermvergrendeling"
                    ),
                },
                {"role": "user", "content": f"{word}{context_line}"},
            ],
            "temperature": 0.0,
        },
    )

    return response.json()["choices"][0]["message"]["content"].strip()
