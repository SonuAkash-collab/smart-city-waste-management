"""Tests for listing, approving, rejecting and cancelling requests (TC-REQ-03, TC-REQ-04)."""

from datetime import datetime, timezone

import pytest

from app.models.collection_request import CollectionRequest, RequestStatus
from app.models.notification import Notification
from app.models.user import UserRole

from tests.test_requests_submit import submit


def set_status(db_session, request_id, status):
    request = db_session.get(CollectionRequest, request_id)
    request.status = status
    db_session.commit()


def ids(response):
    return sorted(item["id"] for item in response.json()["items"])


@pytest.fixture
def mixed_requests(client, citizen_headers, admin_headers, db_session):
    """Five requests with known status, priority, waste type and date."""
    a = submit(client, citizen_headers, wasteType="MIXED").json()["id"]
    b = submit(client, citizen_headers, wasteType="HAZARDOUS").json()["id"]
    c = submit(client, citizen_headers, wasteType="GARDEN").json()["id"]
    d = submit(client, citizen_headers, wasteType="MIXED").json()["id"]
    e = submit(client, citizen_headers, wasteType="MIXED").json()["id"]
    for request_id in (a, b, d):
        client.patch(f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=admin_headers)
    client.patch(
        f"/api/v1/requests/{d}/status", json={"status": "APPROVED", "priority": "HIGH"}, headers=admin_headers
    )
    old = db_session.get(CollectionRequest, e)
    old.status = RequestStatus.REJECTED  # closed, so its priority stays MEDIUM
    old.created_at = datetime(2026, 10, 10, 9, 0, tzinfo=timezone.utc)
    db_session.commit()
    return {"a": a, "b": b, "c": c, "d": d, "e": e}


def test_filter_by_each_field(client, admin_headers, mixed_requests):
    r = mixed_requests
    base = "/api/v1/requests?page=1&size=20"
    assert ids(client.get(f"{base}&status=APPROVED", headers=admin_headers)) == sorted([r["a"], r["b"], r["d"]])
    assert ids(client.get(f"{base}&priority=HIGH", headers=admin_headers)) == sorted([r["b"], r["d"]])
    assert ids(client.get(f"{base}&wasteType=MIXED", headers=admin_headers)) == sorted([r["a"], r["d"], r["e"]])
    assert ids(client.get(f"{base}&date=2026-10-10", headers=admin_headers)) == [r["e"]]


def test_combined_filter_and_page_shape(client, admin_headers, mixed_requests):
    response = client.get(
        "/api/v1/requests?status=APPROVED&priority=HIGH&wasteType=MIXED&page=1&size=20",
        headers=admin_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"items", "page", "size", "total"}
    assert (body["page"], body["size"], body["total"]) == (1, 20, 1)
    assert body["items"][0]["id"] == mixed_requests["d"]
    assert body["items"][0]["priorityOverridden"] is True


def test_paging(client, admin_headers, mixed_requests):
    first = client.get("/api/v1/requests?page=1&size=2", headers=admin_headers).json()
    third = client.get("/api/v1/requests?page=3&size=2", headers=admin_headers).json()
    assert first["total"] == 5 and len(first["items"]) == 2
    assert len(third["items"]) == 1


def test_bad_paging_rejected(client, admin_headers):
    assert client.get("/api/v1/requests?page=0", headers=admin_headers).status_code == 422
    assert client.get("/api/v1/requests?size=500", headers=admin_headers).status_code == 422


def test_citizen_lists_only_own_requests(client, citizen_headers, make_user, headers_for, mixed_requests):
    other = headers_for(make_user(UserRole.CITIZEN))
    mine = submit(client, other).json()["id"]
    assert ids(client.get("/api/v1/requests", headers=other)) == [mine]
    assert client.get("/api/v1/requests", headers=citizen_headers).json()["total"] == 5


def test_approve_then_get(client, citizen_headers, admin_headers):
    request_id = submit(client, citizen_headers).json()["id"]
    response = client.patch(
        f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=admin_headers
    )
    assert response.status_code == 200
    assert set(response.json()) == {"id", "status", "priority", "updatedAt"}
    assert response.json()["status"] == "APPROVED"
    detail = client.get(f"/api/v1/requests/{request_id}", headers=citizen_headers).json()
    assert detail["status"] == "APPROVED"


def test_reject_with_reason(client, citizen_headers, admin_headers):
    request_id = submit(client, citizen_headers).json()["id"]
    response = client.patch(
        f"/api/v1/requests/{request_id}/status",
        json={"status": "REJECTED", "reason": "Outside service area"},
        headers=admin_headers,
    )
    assert response.json()["status"] == "REJECTED"
    detail = client.get(f"/api/v1/requests/{request_id}", headers=admin_headers).json()
    assert detail["reason"] == "Outside service area"


@pytest.mark.parametrize("priority", ["HIGH", "MEDIUM", "LOW"])
def test_admin_priority_override(client, citizen_headers, admin_headers, priority):
    request_id = submit(client, citizen_headers, wasteType="MIXED").json()["id"]
    response = client.patch(
        f"/api/v1/requests/{request_id}/status",
        json={"status": "APPROVED", "priority": priority},
        headers=admin_headers,
    )
    assert response.json()["priority"] == priority
    assert client.get(f"/api/v1/requests/{request_id}", headers=citizen_headers).json()["priority"] == priority


@pytest.mark.parametrize(
    "start", [RequestStatus.SCHEDULED, RequestStatus.COLLECTED, RequestStatus.CANCELLED, RequestStatus.REJECTED]
)
def test_invalid_transition_conflict(client, citizen_headers, admin_headers, db_session, start):
    request_id = submit(client, citizen_headers).json()["id"]
    set_status(db_session, request_id, start)
    response = client.patch(
        f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=admin_headers
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "INVALID_STATUS_TRANSITION"


def test_citizen_cannot_approve(client, citizen_headers):
    request_id = submit(client, citizen_headers).json()["id"]
    response = client.patch(
        f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=citizen_headers
    )
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_status_must_be_approved_or_rejected(client, citizen_headers, admin_headers):
    request_id = submit(client, citizen_headers).json()["id"]
    response = client.patch(
        f"/api/v1/requests/{request_id}/status", json={"status": "COLLECTED"}, headers=admin_headers
    )
    assert response.status_code == 422


def test_other_citizen_cannot_view(client, citizen_headers, make_user, headers_for):
    request_id = submit(client, citizen_headers).json()["id"]
    stranger = headers_for(make_user(UserRole.CITIZEN))
    assert client.get(f"/api/v1/requests/{request_id}", headers=stranger).status_code == 403


def test_unknown_request(client, admin_headers):
    assert client.get("/api/v1/requests/999", headers=admin_headers).status_code == 404
    response = client.patch("/api/v1/requests/999/status", json={"status": "APPROVED"}, headers=admin_headers)
    assert response.status_code == 404


# --- cancellation (TC-REQ-03) -----------------------------------------------


@pytest.mark.parametrize("start", [RequestStatus.SUBMITTED, RequestStatus.APPROVED])
def test_cancel_before_scheduled(client, citizen_headers, db_session, start):
    request_id = submit(client, citizen_headers).json()["id"]
    set_status(db_session, request_id, start)
    response = client.delete(f"/api/v1/requests/{request_id}", headers=citizen_headers)
    assert response.status_code == 200
    assert response.json() == {"id": request_id, "status": "CANCELLED"}
    assert client.get(f"/api/v1/requests/{request_id}", headers=citizen_headers).json()["status"] == "CANCELLED"


@pytest.mark.parametrize(
    "start",
    [
        RequestStatus.SCHEDULED,
        RequestStatus.COLLECTED,
        RequestStatus.REJECTED,
        RequestStatus.MISSED,
        RequestStatus.CANCELLED,
    ],
)
def test_cancel_after_scheduled_conflict(client, citizen_headers, db_session, start):
    request_id = submit(client, citizen_headers).json()["id"]
    set_status(db_session, request_id, start)
    response = client.delete(f"/api/v1/requests/{request_id}", headers=citizen_headers)
    assert response.status_code == 409
    assert client.get(f"/api/v1/requests/{request_id}", headers=citizen_headers).json()["status"] == start.value


def test_cannot_cancel_someone_elses_request(client, citizen_headers, make_user, headers_for):
    request_id = submit(client, citizen_headers).json()["id"]
    stranger = headers_for(make_user(UserRole.CITIZEN))
    assert client.delete(f"/api/v1/requests/{request_id}", headers=stranger).status_code == 403


def test_every_status_change_notifies_owner(client, citizen, citizen_headers, admin_headers, db_session):
    first = submit(client, citizen_headers).json()["id"]
    client.patch(f"/api/v1/requests/{first}/status", json={"status": "APPROVED"}, headers=admin_headers)
    second = submit(client, citizen_headers).json()["id"]
    client.patch(f"/api/v1/requests/{second}/status", json={"status": "REJECTED"}, headers=admin_headers)
    client.delete(f"/api/v1/requests/{first}", headers=citizen_headers)
    messages = [n.message for n in db_session.query(Notification).filter_by(user_id=citizen.id)]
    assert len(messages) == 5  # submitted x2, approved, rejected, cancelled
    assert any(f"#{first}" in m and "APPROVED" in m for m in messages)
    assert any(f"#{second}" in m and "REJECTED" in m for m in messages)
    assert any(f"#{first}" in m and "CANCELLED" in m for m in messages)


def test_override_without_status_change_does_not_notify(client, citizen, citizen_headers, admin_headers, db_session):
    request_id = submit(client, citizen_headers).json()["id"]
    client.patch(f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=admin_headers)
    before = db_session.query(Notification).filter_by(user_id=citizen.id).count()
    client.patch(
        f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED", "priority": "LOW"}, headers=admin_headers
    )
    assert db_session.query(Notification).filter_by(user_id=citizen.id).count() == before
