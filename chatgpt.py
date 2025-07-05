import aiohttp
import os
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL")

async def ask_chatgpt(messages):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": messages,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=body) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise Exception(f"OpenRouter API returned status {resp.status}\n{text}")
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


#-- MADE BY DAI VIET --
