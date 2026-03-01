"""Tests for mail_sender module."""

import smtplib
import ssl
from unittest.mock import MagicMock, patch

import pytest

from mail_sender import send_reply


@patch("mail_sender.smtplib.SMTP_SSL")
def test_send_reply_adds_re_prefix(mock_smtp_cls):
    mock_server = MagicMock()
    mock_smtp_cls.return_value.__enter__ = lambda s: mock_server
    mock_smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

    send_reply(
        smtp_host="smtp.example.com",
        smtp_port=465,
        smtp_user="bot@example.com",
        smtp_password="secret",
        to_address="user@example.com",
        subject="Hello",
        body="Auto-reply body",
    )

    mock_server.sendmail.assert_called_once()
    raw_msg = mock_server.sendmail.call_args[0][2]
    assert "Re: Hello" in raw_msg


@patch("mail_sender.smtplib.SMTP_SSL")
def test_send_reply_no_double_re_prefix(mock_smtp_cls):
    mock_server = MagicMock()
    mock_smtp_cls.return_value.__enter__ = lambda s: mock_server
    mock_smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

    send_reply(
        smtp_host="smtp.example.com",
        smtp_port=465,
        smtp_user="bot@example.com",
        smtp_password="secret",
        to_address="user@example.com",
        subject="Re: Hello",
        body="Body",
    )

    raw_msg = mock_server.sendmail.call_args[0][2]
    assert "Re: Re:" not in raw_msg
    assert "Re: Hello" in raw_msg


@patch("mail_sender.smtplib.SMTP_SSL")
def test_send_reply_sets_auto_submitted_header(mock_smtp_cls):
    mock_server = MagicMock()
    mock_smtp_cls.return_value.__enter__ = lambda s: mock_server
    mock_smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

    send_reply(
        smtp_host="smtp.example.com",
        smtp_port=465,
        smtp_user="bot@example.com",
        smtp_password="secret",
        to_address="user@example.com",
        subject="Test",
        body="Body",
    )

    raw_msg = mock_server.sendmail.call_args[0][2]
    assert "Auto-Submitted: auto-replied" in raw_msg
