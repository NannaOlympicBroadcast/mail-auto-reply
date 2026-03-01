"""Tests for mail_listener module."""

import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mail_listener import get_plain_body, parse_sender, parse_subject


def _make_simple_message(subject: str, from_: str, body: str) -> email.message.Message:
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_
    msg["To"] = "bot@example.com"
    return msg


def _make_multipart_message(subject: str, from_: str, body: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_
    msg["To"] = "bot@example.com"
    msg.attach(MIMEText(body, "plain", "utf-8"))
    msg.attach(MIMEText(f"<p>{body}</p>", "html", "utf-8"))
    return msg


def test_parse_sender_bare_address():
    msg = _make_simple_message("Hi", "user@example.com", "Hello")
    assert parse_sender(msg) == "user@example.com"


def test_parse_sender_name_and_address():
    msg = _make_simple_message("Hi", "Alice <alice@example.com>", "Hello")
    assert parse_sender(msg) == "alice@example.com"


def test_parse_subject():
    msg = _make_simple_message("Test Subject", "a@b.com", "body")
    assert parse_subject(msg) == "Test Subject"


def test_parse_subject_empty():
    msg = email.message.Message()
    assert parse_subject(msg) == "(no subject)"


def test_get_plain_body_simple():
    msg = _make_simple_message("S", "a@b.com", "Hello world")
    assert "Hello world" in get_plain_body(msg)


def test_get_plain_body_multipart():
    msg = _make_multipart_message("S", "a@b.com", "Multipart body")
    assert "Multipart body" in get_plain_body(msg)
