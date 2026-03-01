"""Mail auto-reply bot entry point.

Usage::

    python main.py

Configuration is loaded from a ``.env`` file (see ``.env.example``).
"""

import logging
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

from github_fetcher import build_github_context
from llm_reply import generate_reply
from mail_listener import fetch_unseen_messages, get_plain_body, parse_sender, parse_subject
from mail_sender import send_reply

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

IMAP_HOST = os.environ["IMAP_HOST"]
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
IMAP_USER = os.environ["IMAP_USER"]
IMAP_PASSWORD = os.environ["IMAP_PASSWORD"]
IMAP_MAILBOX = os.getenv("IMAP_MAILBOX", "INBOX")

SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASSWORD = os.environ["SMTP_PASSWORD"]

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "NannaOlympicBroadcast")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))


def main() -> None:
    openai_kwargs: dict = {"api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        openai_kwargs["base_url"] = OPENAI_BASE_URL
    client = OpenAI(**openai_kwargs)

    logger.info("Fetching GitHub context for %s ...", GITHUB_USERNAME)
    github_context = build_github_context(GITHUB_USERNAME)
    logger.info("GitHub context ready (%d chars).", len(github_context))

    logger.info(
        "Starting mail auto-reply bot. Polling every %d seconds.", POLL_INTERVAL
    )

    while True:
        try:
            for _uid, msg in fetch_unseen_messages(
                IMAP_HOST, IMAP_PORT, IMAP_USER, IMAP_PASSWORD, IMAP_MAILBOX
            ):
                sender = parse_sender(msg)
                subject = parse_subject(msg)
                body = get_plain_body(msg)

                logger.info("Processing email from %s — %s", sender, subject)

                reply_body = generate_reply(
                    sender=sender,
                    subject=subject,
                    body=body,
                    github_context=github_context,
                    client=client,
                )

                send_reply(
                    smtp_host=SMTP_HOST,
                    smtp_port=SMTP_PORT,
                    smtp_user=SMTP_USER,
                    smtp_password=SMTP_PASSWORD,
                    to_address=sender,
                    subject=subject,
                    body=reply_body,
                )

                logger.info("Auto-reply sent to %s", sender)

        except Exception:
            logger.exception("Error during mail processing loop")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
