"""Tests for following a request through its whole life (TC-REQ-03, SCW-F-012)."""

from tests.test_routes_api import DAY, add_facility, add_vehicle
from tests.test_requests_submit import submit


def test_status_follows_the_request_to_collection(client, citizen_headers, admin_headers, driver_headers, db_session, driver):
    add_vehicle(db_session, driver)
    add_facility(db_session)
    request_id = submit(client, citizen_headers, wasteType="MIXED").json()["id"]

    def detail():
        return client.get(f"/api/v1/requests/{request_id}", headers=citizen_headers).json()

    assert detail()["status"] == "SUBMITTED"
    assert detail()["scheduledDate"] is None

    client.patch(f"/api/v1/requests/{request_id}/status", json={"status": "APPROVED"}, headers=admin_headers)
    assert detail()["status"] == "APPROVED"

    route = client.post("/api/v1/routes/generate", json={"date": DAY}, headers=admin_headers).json()["routes"][0]
    assert detail()["status"] == "SCHEDULED"
    assert detail()["scheduledDate"] == DAY
    assert detail()["routeId"] == route["id"]

    # Scheduled requests can no longer be cancelled.
    assert client.delete(f"/api/v1/requests/{request_id}", headers=citizen_headers).status_code == 409

    stop = next(s for s in route["stops"] if s["requestId"] == request_id)
    client.patch(f"/api/v1/routes/{route['id']}/stops/{stop['id']}", json={"status": "COLLECTED"}, headers=driver_headers)
    assert detail()["status"] == "COLLECTED"


def test_my_requests_list_shows_latest_first(client, citizen_headers):
    first = submit(client, citizen_headers).json()["id"]
    second = submit(client, citizen_headers).json()["id"]
    items = client.get("/api/v1/requests", headers=citizen_headers).json()["items"]
    assert [i["id"] for i in items] == [second, first]
    assert {"status", "priority", "wasteType", "createdAt", "hasPhoto"} <= set(items[0])
