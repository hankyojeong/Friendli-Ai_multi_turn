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
    system_prompt: str,
    user_question: str,
    *,
    history: Optional[List[Dict[str, str]]] = None,
    user_reply: Optional[str] = None,
    multi_turn: bool = False,
    **kw,
) -> Dict[str, object]:
    """Call LLM and return whether more user input is required.

    Parameters
    ----------
    client : OpenAI
        OpenAI client instance.
    model : str
        Model name.
    system_prompt : str
        Prompt describing the task and available metadata.
    user_question : str
        The original question from user. Used when ``history`` is empty.
    history : list of dict, optional
        Previous conversation messages excluding the system prompt.
    user_reply : str, optional
        Reply from the user for a follow-up question.
    multi_turn : bool, optional
        If True, the assistant may ask follow-up questions when the
        request is ambiguous.

    Returns
    -------
    dict
        {"content": str, "needs_reply": bool}
    """
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt}
    ]
    if history:
        messages.extend(history)

    if user_reply is not None:
        messages.append({"role": "user", "content": user_reply})
    else:
        messages.append({"role": "user", "content": user_question})

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        **kw
    )
    content = resp.choices[0].message.content
    needs_reply = multi_turn and "```" not in content

    return {
        "content": content,
        "needs_reply": needs_reply,
    }

