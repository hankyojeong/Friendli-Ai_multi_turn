import os
from typing import Optional, List, Dict
from openai import OpenAI


def make_client(
    api_key: Optional[str] = None,
    team_id: Optional[str] = None,
    base_url: str = "https://api.friendli.ai/serverless/v1",
) -> OpenAI:
    api_key = api_key or os.getenv("FRIENDLI_API_KEY", "REPLACE_ME")
    team_id = team_id or os.getenv("FRIENDLI_TEAM_ID", "REPLACE_ME")
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers={"x-friendli-team": team_id},
    )


def call_llm(
    client: OpenAI,
    model: str,
    *,
    history: List[Dict[str, str]],
    user_reply: Optional[str] = None,
    **kw,
) -> Dict[str, str | bool]:
    """Call LLM with externally provided conversation history.

    Parameters
    ----------
    client : OpenAI
        OpenAI client instance.
    model : str
        Model name.
    history : list[dict]
        Existing conversation messages.
    user_reply : str | None, optional
        Latest user response to append before calling the model.

    Returns
    -------
    dict
        A dictionary containing ``needs_reply`` and ``content`` keys.
    """

    messages = list(history)
    if user_reply is not None:
        messages.append({"role": "user", "content": user_reply})

    resp = client.chat.completions.create(
        model=model, messages=messages, **kw
    )
    content = resp.choices[0].message.content

    needs_reply = "```" not in content
    return {"needs_reply": needs_reply, "content": content}
