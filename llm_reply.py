"""Generate an auto-reply email body using an LLM."""

from openai import OpenAI

SYSTEM_PROMPT = """你是 NannaOlympicBroadcast 的自动回复助手。

重要提示：本人目前正在全力备考研究生入学考试（考研），无法及时回复邮件，请勿打扰。

你的任务：
1. 根据来信内容，结合下方提供的 GitHub 公开项目信息，给出简洁、有帮助的自动回复。
2. 如果来信是技术问题，请根据相关项目信息给出指引或建议。
3. 在回复的结尾务必说明：本人正在备考研究生入学考试，暂时无法亲自回复，如有紧急事项请稍后再联系。
4. 语气礼貌、专业，中英文均可，根据来信语言选择回复语言。

以下是本人的 GitHub 公开项目信息供参考：
{github_context}
"""


def generate_reply(
    sender: str,
    subject: str,
    body: str,
    github_context: str,
    client: OpenAI,
    model: str = "gpt-4o-mini",
) -> str:
    """Generate an auto-reply using the LLM.

    Parameters
    ----------
    sender:
        Email address of the original sender.
    subject:
        Subject line of the incoming email.
    body:
        Plain-text body of the incoming email.
    github_context:
        Pre-built context string from :func:`github_fetcher.build_github_context`.
    client:
        An instantiated :class:`openai.OpenAI` client.
    model:
        The chat model to use (default ``gpt-4o-mini``).
    """
    system = SYSTEM_PROMPT.format(github_context=github_context)
    user_message = (
        f"来信发件人：{sender}\n"
        f"主题：{subject}\n\n"
        f"内容：\n{body}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""
