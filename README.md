# mail-auto-reply

> ⚠️ **本人目前正在全力备考研究生入学考试（考研），无法及时回复邮件，敬请谅解，请勿打扰。**
>
> The owner of this account is currently preparing for graduate school entrance exams and is unavailable. Please do not disturb.

---

An intelligent mail auto-reply bot that:

- **Listens** to an IMAP inbox for new incoming emails.
- **Fetches** the owner's public GitHub projects and profile info ([NannaOlympicBroadcast](https://github.com/NannaOlympicBroadcast)) as context.
- **Generates** a helpful, context-aware reply using an LLM (OpenAI-compatible API).
- **Sends** the auto-reply back to the original sender via SMTP.
- Always reminds senders that the owner is currently focused on graduate school entrance exam preparation.

---

## Project structure

```
mail-auto-reply/
├── main.py              # Entry point – polling loop
├── mail_listener.py     # IMAP listener & email parsing utilities
├── mail_sender.py       # SMTP sender
├── github_fetcher.py    # Fetch NannaOlympicBroadcast's public GitHub info
├── llm_reply.py         # LLM-based reply generation (OpenAI API)
├── requirements.txt
├── .env.example         # Configuration template
└── tests/
    ├── test_github_fetcher.py
    ├── test_llm_reply.py
    ├── test_mail_listener.py
    └── test_mail_sender.py
```

---

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/NannaOlympicBroadcast/mail-auto-reply.git
cd mail-auto-reply
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `IMAP_HOST` | IMAP server hostname (e.g. `imap.gmail.com`) |
| `IMAP_PORT` | IMAP SSL port (default: `993`) |
| `IMAP_USER` | Your email address |
| `IMAP_PASSWORD` | Your email password / app password |
| `IMAP_MAILBOX` | Mailbox to monitor (default: `INBOX`) |
| `SMTP_HOST` | SMTP server hostname (e.g. `smtp.gmail.com`) |
| `SMTP_PORT` | SMTP SSL port (default: `465`) |
| `SMTP_USER` | Your email address |
| `SMTP_PASSWORD` | Your email password / app password |
| `OPENAI_API_KEY` | OpenAI API key |
| `OPENAI_BASE_URL` | *(optional)* Custom OpenAI-compatible base URL |
| `GITHUB_USERNAME` | GitHub username for context (default: `NannaOlympicBroadcast`) |
| `POLL_INTERVAL` | Seconds between inbox checks (default: `60`) |

### 3. Run

```bash
python main.py
```

The bot will start polling the IMAP inbox every `POLL_INTERVAL` seconds. When a new (unseen) email arrives it will:

1. Parse the sender address and subject.
2. Fetch the latest GitHub context (once at startup).
3. Call the LLM to generate a personalized reply that includes a note about 考研.
4. Send the reply via SMTP.

---

## Running tests

```bash
pip install pytest
pytest tests/
```

---

## Notes

- The bot marks processed emails as **seen** so they are not replied to again.
- All LLM replies will include a notice that the mailbox owner is currently preparing for graduate school entrance exams and cannot respond personally.
- For Gmail, you need to enable IMAP and use an [App Password](https://support.google.com/accounts/answer/185833).
