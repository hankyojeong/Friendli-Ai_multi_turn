from typing import List, Dict, Optional
from openai import OpenAI


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
# In this repository we avoid the use of environment variables so that the
# project can be run without additional shell configuration.  Replace the
# following placeholder values with your actual credentials.  They will be used
# as the defaults when creating an ``OpenAI`` client.
DEFAULT_API_KEY = "YOUR_API_KEY"
DEFAULT_TEAM_ID = "YOUR_TEAM_ID"


def make_client(
    api_key: str = DEFAULT_API_KEY,
    team_id: str = DEFAULT_TEAM_ID,
    base_url: str = "https://api.friendli.ai/serverless/v1",
) -> OpenAI:
    """Construct an :class:`OpenAI` client.

    Parameters
    ----------
    api_key:
        API key used for authentication.  Defaults to ``DEFAULT_API_KEY`` defined
        in this module.
    team_id:
        Team identifier to be sent as ``x-friendli-team`` header.  Defaults to
        ``DEFAULT_TEAM_ID``.
    base_url:
        Base URL for the Friendli serverless endpoint.
    """

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

