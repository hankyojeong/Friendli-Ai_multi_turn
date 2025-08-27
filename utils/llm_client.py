import os
from typing import Optional, List, Dict
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

def call_llm(client: OpenAI, model: str, messages: List[Dict[str, str]], **kw) -> str:
    """Send a chat completion request with an explicit message list."""
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        **kw,
    )
    return resp.choices[0].message.content
