import csv
import json
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_URL = os.getenv("LM_STUDIO_URL")
CSV_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "output", "evaluations.csv"
)
CSV_HEADERS = [
    "timestamp",
    "question",
    "answer",
    "chunks",
    "faithfulness",
    "relevance",
    "verdict",
]


def evaluate(question: str, answer: str, chunks: list[dict]) -> None:
    """Evaluate the RAG answer using LLM-as-a-judge, print the result, and append to CSV."""

    context = "\n\n".join(f"{chunk['title']}:\n{chunk['content']}" for chunk in chunks)

    response = requests.post(
        LM_STUDIO_URL,
        json={
            "model": "local-model",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an evaluator for a RAG (Retrieval-Augmented Generation) system. "
                        "Given a question, an answer, and the source chunks used to generate the answer, "
                        "evaluate the answer on two criteria and respond with JSON only:\n\n"
                        "1. faithfulness (0.0–1.0): Is every claim in the answer supported by the provided chunks?\n"
                        "2. relevance (0.0–1.0): Does the answer actually address the question?\n\n"
                        "Respond with exactly this JSON format, nothing else:\n"
                        '{"faithfulness": <score>, "relevance": <score>, "verdict": "<one sentence>"}'
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Question: {question}\n\n"
                        f"Answer: {answer}\n\n"
                        f"Source chunks:\n{context}"
                    ),
                },
            ],
            "temperature": 0.0,
        },
    )

    result = response.json()["choices"][0]["message"]["content"].strip()
    print(f"\n[RAG Evaluation]\n{result}\n")

    try:
        scores = json.loads(result)
    except json.JSONDecodeError:
        scores = {"faithfulness": None, "relevance": None, "verdict": result}

    csv_path = os.path.abspath(CSV_PATH)
    write_header = not os.path.exists(csv_path)

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now().isoformat(),
                "question": question,
                "answer": answer,
                "chunks": json.dumps(
                    [{"id": c["id"], "title": c["title"]} for c in chunks]
                ),
                "faithfulness": scores.get("faithfulness"),
                "relevance": scores.get("relevance"),
                "verdict": scores.get("verdict"),
            }
        )
