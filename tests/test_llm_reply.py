"""Tests for llm_reply module."""

from unittest.mock import MagicMock

from llm_reply import generate_reply, SYSTEM_PROMPT


GITHUB_CTX = "GitHub user: NannaOlympicBroadcast\nPublic repositories: 2"


def _make_openai_client(reply_text: str) -> MagicMock:
    choice = MagicMock()
    choice.message.content = reply_text
    completion = MagicMock()
    completion.choices = [choice]
    client = MagicMock()
    client.chat.completions.create.return_value = completion
    return client


def test_generate_reply_returns_string():
    client = _make_openai_client("Auto-reply text")
    result = generate_reply(
        sender="user@example.com",
        subject="Question about your project",
        body="How do I use clawdbot?",
        github_context=GITHUB_CTX,
        client=client,
    )
    assert result == "Auto-reply text"


def test_generate_reply_passes_github_context():
    client = _make_openai_client("ok")
    generate_reply(
        sender="a@b.com",
        subject="Hi",
        body="Hello",
        github_context=GITHUB_CTX,
        client=client,
    )
    call_args = client.chat.completions.create.call_args
    messages = call_args.kwargs["messages"]
    system_msg = next(m for m in messages if m["role"] == "system")
    assert GITHUB_CTX in system_msg["content"]


def test_system_prompt_contains_kaoyan():
    assert "考研" in SYSTEM_PROMPT
