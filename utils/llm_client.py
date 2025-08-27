import os
from typing import Optional
from openai import OpenAI

def make_client(api_key: Optional[str] = None,
                team_id: Optional[str] = None,
                base_url: str = "https://api.friendli.ai/serverless/v1") -> OpenAI:
    api_key = api_key or os.getenv("FRIENDLI_API_KEY", "REPLACE_ME")
    team_id = team_id or os.getenv("FRIENDLI_TEAM_ID", "REPLACE_ME")
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers={"x-friendli-team": team_id},
    )

def call_llm(client: OpenAI, model: str, system_prompt: str, user_text: str, **kw) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        **kw
    )
    return resp.choices[0].message.content
