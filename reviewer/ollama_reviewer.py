import requests
from typer import prompt

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "codellama:7b"


def review_with_ollama(code: str) -> str:
    """
    Sends code to a locally running Ollama model (CodeLlama)
    and returns a code review.
    """

    prompt = f"""
You are a senior Python software engineer.

Review the following Python code and provide:
- Bugs
- Security issues
- Bad practices
- Performance issues
- Suggestions for improvement

Respond in clear bullet points.

CODE:
```python
{code}
"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)

    if response.status_code != 200:
        raise RuntimeError("Ollama request failed")

    return response.json().get("response", "").strip()

