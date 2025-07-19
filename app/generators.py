import os

from openai import AsyncOpenAI
from dotenv import load_dotenv
load_dotenv()

client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv('AI_API_KEY2'),
)


async def ai_generate(req):
    completion = await client.chat.completions.create(
        extra_body={},
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[
            {
                "role": "user",
                "content": req,
                "temterature": "0.0"
            }
        ]
      )
    return completion.choices[0].message.content