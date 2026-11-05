"""Tests for the audit log of Admin actions (TC-SEC-04)."""

from app.models.audit_log import AuditLog
from tests.test_requests_submit import submit
from tests.test_routes_api import add_request, add_vehicle


def entries(db_session):
    return db_session.query(AuditLog).order_by(AuditLog.id).all()


def test_admin_actions_are_recorded(client, admin, admin_headers, citizen, citizen_headers, driver, db_session):
    approved = submit(client, citizen_headers).json()["id"]
    rejected = submit(client, citizen_headers).json()["id"]
    client.patch(f"/api/v1/requests/{approved}/status", json={"status": "APPROVED"}, headers=admin_headers)
    client.patch(f"/api/v1/requests/{rejected}/status", json={"status": "REJECTED"}, headers=admin_headers)
    add_vehicle(db_session, driver)
    client.post("/api/v1/routes/generate", json={"date": "2026-11-02"}, headers=admin_headers)
    client.patch(f"/api/v1/users/{driver.id}/status", json={"isActive": False}, headers=admin_headers)

    log = entries(db_session)
    assert [e.action for e in log] == [
        "REQUEST_DECIDED", "REQUEST_DECIDED", "ROUTES_GENERATED", "ACCOUNT_STATUS_CHANGED",
    ]
    assert [e.entity_id for e in log] == [approved, rejected, None, driver.id]
    assert all(e.user_id == admin.id and e.created_at is not None for e in log)


def test_failed_and_non_admin_calls_not_recorded(client, admin_headers, citizen_headers, db_session):
    client.patch("/api/v1/requests/999/status", json={"status": "APPROVED"}, headers=admin_headers)  # 404
    submit(client, citizen_headers)  # citizen action, not an admin action
    client.get("/api/v1/requests", headers=admin_headers)  # reading changes nothing
    assert entries(db_session) == []


def test_admin_reads_audit_log(client, admin, admin_headers, citizen, db_session):
    add_request(db_session, citizen, 0.01)
    client.post("/api/v1/routes/generate", json={"date": "2026-11-02"}, headers=admin_headers)
    rows = client.get("/api/v1/audit", headers=admin_headers).json()
    assert rows[0]["action"] == "ROUTES_GENERATED"
    assert rows[0]["actorName"] == admin.full_name
    assert rows[0]["createdAt"].endswith("Z")


def test_audit_log_is_admin_only(client, citizen_headers, operator_headers):
    assert client.get("/api/v1/audit", headers=citizen_headers).status_code == 403
    assert client.get("/api/v1/audit", headers=operator_headers).status_code == 403
