"""Tests for in-app and email notifications (TC-NOT-01, SCW-F-050)."""

import pytest

from app.services import mailer
from tests.test_requests_submit import submit


@pytest.fixture(autouse=True)
def clear_mail():
    mailer.sent_messages.clear()


def test_every_status_change_reaches_owner_in_app_and_by_email(client, citizen, citizen_headers, admin_headers):
    first = submit(client, citizen_headers, wasteType="MIXED", estimatedQuantityKg=20).json()["id"]
    client.patch(f"/api/v1/requests/{first}/status", json={"status": "APPROVED"}, headers=admin_headers)
    second = submit(client, citizen_headers, wasteType="MIXED", estimatedQuantityKg=20).json()["id"]
    client.patch(f"/api/v1/requests/{second}/status", json={"status": "REJECTED"}, headers=admin_headers)

    body = client.get("/api/v1/notifications", headers=citizen_headers).json()
    messages = [n["message"] for n in body["items"]]
    assert len(messages) == 4 and body["unread"] == 4
    for request_id, status in [(first, "SUBMITTED"), (first, "APPROVED"), (second, "SUBMITTED"), (second, "REJECTED")]:
        assert any(f"#{request_id}" in m and status in m and "UTC" in m for m in messages)

    emails = [m for m in mailer.sent_messages if m["to"] == citizen.email]
    assert sorted(e["body"] for e in emails) == sorted(messages)


def test_no_one_else_is_notified(client, citizen_headers, admin_headers, make_user, headers_for):
    from app.models.user import UserRole

    other = headers_for(make_user(UserRole.CITIZEN))
    submit(client, citizen_headers)
    assert client.get("/api/v1/notifications", headers=other).json()["items"] == []


def test_mark_one_and_all_read(client, citizen_headers):
    submit(client, citizen_headers)
    submit(client, citizen_headers)
    items = client.get("/api/v1/notifications", headers=citizen_headers).json()["items"]
    one = client.patch(f"/api/v1/notifications/{items[0]['id']}/read", headers=citizen_headers)
    assert one.json()["isRead"] is True
    assert client.get("/api/v1/notifications?unread=true", headers=citizen_headers).json()["unread"] == 1
    client.post("/api/v1/notifications/read-all", headers=citizen_headers)
    assert client.get("/api/v1/notifications", headers=citizen_headers).json()["unread"] == 0


def test_cannot_read_someone_elses_notification(client, citizen_headers, driver_headers):
    submit(client, citizen_headers)
    note = client.get("/api/v1/notifications", headers=citizen_headers).json()["items"][0]
    assert client.patch(f"/api/v1/notifications/{note['id']}/read", headers=driver_headers).status_code == 404


def test_email_failure_does_not_block(monkeypatch, client, citizen_headers):
    monkeypatch.setenv("SMTP_HOST", "127.0.0.1")
    monkeypatch.setenv("SMTP_PORT", "1")  # nothing listens here
    assert submit(client, citizen_headers).status_code == 201
    assert client.get("/api/v1/notifications", headers=citizen_headers).json()["unread"] == 1


def test_outbox_file_written(tmp_path, monkeypatch):
    outbox = tmp_path / "outbox.log"
    monkeypatch.setenv("EMAIL_OUTBOX", str(outbox))
    assert mailer.send_email("a@test.local", "Hi", "Request #1: status is now APPROVED")
    assert "Request #1" in outbox.read_text(encoding="utf-8")
