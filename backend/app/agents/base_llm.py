import httpx
from app.config import OPENAI_API_KEY, MODEL_NAME

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

async def call_openai(system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(OPENAI_API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
