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
    system_prompt: Optional[str] = None,
    user_question: Optional[str] = None,
    *,
    messages: Optional[List[Dict[str, str]]] = None,
    multi_turn: bool = False,
    max_turns: int = 5,
    **kw,
) -> str:
    """Call the LLM and return the assistant's message.

    This refactored version accepts either a complete ``messages`` list or a
    ``system_prompt``/``user_question`` pair for convenience.  The previous
    interactive ``multi_turn`` behaviour has been removed; the related
    arguments are retained for backward compatibility but are otherwise
    ignored.

    Parameters
    ----------
    client : OpenAI
        OpenAI client instance.
    model : str
        Model name.
    system_prompt : str, optional
        Prompt describing the task.  Used only when ``messages`` is ``None``.
    user_question : str, optional
        User input for single-turn calls.  Used only when ``messages`` is
        ``None``.
    messages : list of dict, optional
        Full conversation to send to the model.  If omitted, a single-turn
        conversation is constructed from ``system_prompt`` and ``user_question``.

    Returns
    -------
    str
        Final assistant message.
    """

    if messages is None:
        if system_prompt is None or user_question is None:
            raise ValueError(
                "system_prompt and user_question are required when messages is None"
            )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ]

    resp = client.chat.completions.create(model=model, messages=messages, **kw)
    return resp.choices[0].message.content
