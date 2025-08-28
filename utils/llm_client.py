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
    multi_turn: bool = False,
    max_turns: int = 5,
    **kw,
) -> str:
    """Call LLM with optional multi-turn clarification.

    Parameters
    ----------
    client : OpenAI
        OpenAI client instance.
    model : str
        Model name.
    system_prompt : str
        Prompt describing the task and available metadata.
    user_question : str
        The original question from user.
    multi_turn : bool, optional
        If True, the assistant may ask follow-up questions when the
        request is ambiguous. Conversation continues until the model
        returns a message containing a code block or the maximum number
        of turns is reached.
    max_turns : int, optional
        Maximum number of clarification turns.

    Returns
    -------
    str
        Final assistant message (expected to include code block).
    """

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question},
    ]

    for _ in range(max_turns):
        resp = client.chat.completions.create(
            model=model, messages=messages, **kw
        )
        content = resp.choices[0].message.content
        messages.append({"role": "assistant", "content": content})

        if multi_turn and "```" not in content:
            # LLM is likely asking for clarification
            print(content)
            user_reply = input("User: ")
            messages.append({"role": "user", "content": user_reply})
            continue

        return content

    raise RuntimeError("Max turns exceeded without reaching final answer")
