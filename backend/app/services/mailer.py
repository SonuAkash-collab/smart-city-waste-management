"""Email delivery for notifications (SCW-F-050).

If SMTP_HOST is set, mail goes through that SMTP server (for example MailHog
on localhost:1025 during testing). Otherwise each email is appended to a local
outbox file (EMAIL_OUTBOX, default ``email-outbox.log``) so the demo works
without a mail server. A failed email never blocks the in-app notification.
"""

import logging
import os
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

logger = logging.getLogger("scw.mail")
SENDER = os.getenv("EMAIL_FROM", "no-reply@scw.local")
sent_messages: list[dict] = []  # kept in memory too, for tests


def send_email(to: str, subject: str, body: str) -> bool:
    record = {"to": to, "subject": subject, "body": body, "at": datetime.now(timezone.utc).isoformat()}
    try:
        host = os.getenv("SMTP_HOST")
        if host:
            message = EmailMessage()
            message["From"], message["To"], message["Subject"] = SENDER, to, subject
            message.set_content(body)
            with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", "25")), timeout=10) as smtp:
                smtp.send_message(message)
        else:
            with open(os.getenv("EMAIL_OUTBOX", "email-outbox.log"), "a", encoding="utf-8") as outbox:
                outbox.write(f"[{record['at']}] To: {to} | {subject} | {body}\n")
        sent_messages.append(record)
        return True
    except OSError:
        logger.exception("Email to %s failed", to)
        return False
