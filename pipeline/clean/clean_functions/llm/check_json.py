import json


def check_json(raw: str, expected_length: int) -> bool:
    """Checks if the LLM response is valid JSON and contains the expected number of items."""

    try:
        result = json.loads(raw)
        return isinstance(result, list) and len(result) == expected_length
    except (json.JSONDecodeError, ValueError):
        return False
