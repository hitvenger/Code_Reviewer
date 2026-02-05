"""from huggingface_hub import InferenceClient
import os

MODEL = "bigcode/starcoder"

client = InferenceClient(
    model=MODEL,
    token=os.getenv("HF_API_KEY")
)

def review_with_hf(code: str) -> str:
    prompt = f"
You are a senior Python developer.

Review the following code and list:
- Bugs
- Bad practices
- Security risks
- Improvements

Respond in bullet points.

CODE:
{code}
""

    response = client.text_generation(
        prompt,
        max_new_tokens=400,
        temperature=0.2,
        do_sample=False
    )

    return response
"""