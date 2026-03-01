"""IMAP-based email listener.

Polls the configured mailbox at regular intervals and yields
unread :class:`email.message.Message` objects.
"""

import email
import imaplib
import logging
from email.message import Message
from typing import Generator

logger = logging.getLogger(__name__)


def _decode_header_value(value: str) -> str:
    """Decode a potentially encoded email header value to a plain string."""
    parts = email.header.decode_header(value)
    decoded = []
    for part, charset in parts:
        if isinstance(part, bytes):
            decoded.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(part)
    return "".join(decoded)


def get_plain_body(msg: Message) -> str:
    """Extract the plain-text body from a :class:`email.message.Message`."""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if ct == "text/plain" and "attachment" not in cd:
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="replace")
    else:
        charset = msg.get_content_charset() or "utf-8"
        return msg.get_payload(decode=True).decode(charset, errors="replace")
    return ""


def fetch_unseen_messages(
    imap_host: str,
    imap_port: int,
    imap_user: str,
    imap_password: str,
    mailbox: str = "INBOX",
) -> Generator[tuple[bytes, Message], None, None]:
    """Connect to an IMAP server and yield ``(uid, message)`` for each unseen email.

    The message is marked as *seen* after being yielded so it is not processed
    again on the next poll.

    Parameters
    ----------
    imap_host / imap_port:
        IMAP server connection details (SSL).
    imap_user / imap_password:
        Login credentials.
    mailbox:
        Mailbox/folder to monitor (default ``INBOX``).
    """
    with imaplib.IMAP4_SSL(imap_host, imap_port) as imap:
        imap.login(imap_user, imap_password)
        imap.select(mailbox)

        status, data = imap.uid("search", None, "UNSEEN")
        if status != "OK" or not data[0]:
            return

        uids = data[0].split()
        logger.info("Found %d unseen message(s).", len(uids))

        for uid in uids:
            status, msg_data = imap.uid("fetch", uid, "(RFC822)")
            if status != "OK":
                logger.warning("Failed to fetch UID %s", uid)
                continue

            raw = msg_data[0][1]
            msg = email.message_from_bytes(raw)

            # Mark as seen
            imap.uid("store", uid, "+FLAGS", "\\Seen")

            yield uid, msg


def parse_sender(msg: Message) -> str:
    """Return the sender email address from a message."""
    from_header = _decode_header_value(msg.get("From", ""))
    # Extract bare address if "Name <addr>" format
    if "<" in from_header and ">" in from_header:
        return from_header[from_header.index("<") + 1 : from_header.index(">")].strip()
    return from_header.strip()


def parse_subject(msg: Message) -> str:
    """Return the decoded subject of a message."""
    return _decode_header_value(msg.get("Subject", "(no subject)"))
