"""Tests for submitting requests and priority rules (TC-REQ-01, TC-REQ-02)."""

import base64
from datetime import timedelta

import pytest

from app.models.collection_request import CollectionRequest, Priority, RequestStatus
from app.models.notification import Notification
from app.services.requests import escalate_waiting_requests, utcnow

PHOTO = base64.b64encode(b"\x89PNG\r\n\x1a\n fake image bytes").decode()


def payload(**overrides):
    body = {
        "latitude": 12.97,
        "longitude": 77.59,
        "address": "MG Road, Bengaluru",
        "wasteType": "HAZARDOUS",
        "estimatedQuantityKg": 25,
    }
    body.update(overrides)
    return body


def submit(client, headers, **overrides):
    return client.post("/api/v1/requests", json=payload(**overrides), headers=headers)


def test_submit_without_photo(client, citizen_headers):
    response = submit(client, citizen_headers)
    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"id", "status", "priority", "createdAt"}
    assert body["status"] == "SUBMITTED"
    assert body["priority"] == "HIGH"
    assert body["createdAt"].endswith("Z")


def test_submit_with_photo_and_read_it_back(client, citizen_headers):
    created = submit(client, citizen_headers, photo=PHOTO)
    assert created.status_code == 201
    detail = client.get(f"/api/v1/requests/{created.json()['id']}", headers=citizen_headers)
    assert detail.status_code == 200
    assert detail.json()["hasPhoto"] is True
    assert detail.json()["photo"] == PHOTO


def test_missing_location_rejected(client, citizen_headers):
    body = payload()
    for key in ("latitude", "longitude", "address"):
        body.pop(key)
    response = client.post("/api/v1/requests", json=body, headers=citizen_headers)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "LOCATION_REQUIRED"


def test_address_without_coordinates_rejected(client, citizen_headers):
    response = client.post(
        "/api/v1/requests",
        json={"address": "Somewhere", "wasteType": "MIXED", "estimatedQuantityKg": 5},
        headers=citizen_headers,
    )
    assert response.json()["error"]["code"] == "LOCATION_REQUIRED"


def test_bad_photo_rejected(client, citizen_headers):
    response = submit(client, citizen_headers, photo="not base64 !!")
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_PHOTO"


@pytest.mark.parametrize("quantity", [0, -5, 20000])
def test_bad_quantity_rejected(client, citizen_headers, quantity):
    assert submit(client, citizen_headers, estimatedQuantityKg=quantity).status_code == 422


def test_unknown_waste_type_rejected(client, citizen_headers):
    assert submit(client, citizen_headers, wasteType="GENERAL").status_code == 422


@pytest.mark.parametrize(
    "waste, expected",
    [
        ("HAZARDOUS", "HIGH"),
        ("MEDICAL", "HIGH"),
        ("E_WASTE", "HIGH"),
        ("MIXED", "MEDIUM"),
        ("RECYCLABLE", "MEDIUM"),
        ("GARDEN", "LOW"),
        ("BULKY", "LOW"),
    ],
)
def test_priority_from_waste_type(client, citizen_headers, waste, expected):
    assert submit(client, citizen_headers, wasteType=waste).json()["priority"] == expected


def test_submit_needs_login(client):
    assert client.post("/api/v1/requests", json=payload()).status_code == 401


def test_only_citizens_submit(client, admin_headers, driver_headers):
    assert submit(client, admin_headers).status_code == 403
    assert submit(client, driver_headers).status_code == 403


def test_submit_notifies_owner(client, citizen, citizen_headers, db_session):
    request_id = submit(client, citizen_headers).json()["id"]
    notes = db_session.query(Notification).filter_by(user_id=citizen.id).all()
    assert len(notes) == 1
    assert f"Request #{request_id}" in notes[0].message
    assert "SUBMITTED" in notes[0].message


# --- 48-hour escalation (TC-REQ-02 step 2) -----------------------------------


def age(db_session, request_id, hours):
    request = db_session.get(CollectionRequest, request_id)
    request.created_at = utcnow() - timedelta(hours=hours)
    db_session.commit()
    return request


@pytest.mark.parametrize(
    "waste, before, after",
    [("GARDEN", "LOW", "MEDIUM"), ("MIXED", "MEDIUM", "HIGH"), ("HAZARDOUS", "HIGH", "HIGH")],
)
def test_waiting_request_goes_up_one_level(client, citizen_headers, db_session, waste, before, after):
    created = submit(client, citizen_headers, wasteType=waste).json()
    assert created["priority"] == before
    age(db_session, created["id"], 49)
    detail = client.get(f"/api/v1/requests/{created['id']}", headers=citizen_headers).json()
    assert detail["priority"] == after


def test_escalation_happens_only_once(client, citizen_headers, db_session):
    request_id = submit(client, citizen_headers, wasteType="GARDEN").json()["id"]
    age(db_session, request_id, 100)
    assert escalate_waiting_requests(db_session) == 1
    assert escalate_waiting_requests(db_session) == 0
    assert db_session.get(CollectionRequest, request_id).priority == Priority.MEDIUM


def test_young_request_not_escalated(client, citizen_headers, db_session):
    request_id = submit(client, citizen_headers, wasteType="GARDEN").json()["id"]
    age(db_session, request_id, 47)
    assert escalate_waiting_requests(db_session) == 0


def test_approved_request_also_escalates(client, citizen_headers, admin_headers, db_session):
    request_id = submit(client, citizen_headers, wasteType="BULKY").json()["id"]
    client.patch(f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=admin_headers)
    age(db_session, request_id, 49)
    assert client.get(f"/api/v1/requests/{request_id}", headers=admin_headers).json()["priority"] == "MEDIUM"


def test_closed_and_overridden_requests_not_escalated(client, citizen_headers, admin_headers, db_session):
    rejected = submit(client, citizen_headers, wasteType="GARDEN").json()["id"]
    client.patch(f"/api/v1/requests/{rejected}/status", json={"status": "REJECTED"}, headers=admin_headers)
    overridden = submit(client, citizen_headers, wasteType="MIXED").json()["id"]
    client.patch(
        f"/api/v1/requests/{overridden}/status",
        json={"status": "APPROVED", "priority": "LOW"},
        headers=admin_headers,
    )
    age(db_session, rejected, 72)
    age(db_session, overridden, 72)
    assert escalate_waiting_requests(db_session) == 0
    assert db_session.get(CollectionRequest, rejected).status == RequestStatus.REJECTED
    assert db_session.get(CollectionRequest, overridden).priority == Priority.LOW
