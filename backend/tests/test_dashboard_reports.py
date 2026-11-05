"""Tests for the admin dashboard and the daily CSV report (TC-RPT-01)."""

import csv
import io

from app.models.collection_request import RequestStatus
from app.models.vehicle import VehicleStatus
from app.services.reports import COLUMNS
from tests.test_routes_api import DAY, add_facility, add_request, add_vehicle, generate


def test_dashboard_counts_match_records(client, admin_headers, db_session, citizen, driver, make_user):
    from app.models.user import UserRole

    add_vehicle(db_session, driver)
    add_vehicle(db_session, make_user(UserRole.DRIVER), reg="KA02", status=VehicleStatus.MAINTENANCE)
    add_facility(db_session, capacity=2000)
    add_request(db_session, citizen, 0.01, "HAZARDOUS", status=RequestStatus.SUBMITTED)
    add_request(db_session, citizen, 0.02, "GARDEN", status=RequestStatus.SUBMITTED)
    add_request(db_session, citizen, 0.03, "MIXED", status=RequestStatus.APPROVED)
    add_request(db_session, citizen, 0.04, "MIXED", status=RequestStatus.REJECTED)

    body = client.get("/api/v1/dashboard", headers=admin_headers).json()
    assert body["requestsByStatus"]["SUBMITTED"] == 2
    assert body["requestsByStatus"]["APPROVED"] == 1
    assert body["requestsByStatus"]["REJECTED"] == 1
    assert body["requestsByStatus"]["COLLECTED"] == 0
    assert body["pendingByPriority"] == {"HIGH": 1, "MEDIUM": 0, "LOW": 1}
    assert body["vehiclesByStatus"] == {"AVAILABLE": 1, "ON_ROUTE": 0, "MAINTENANCE": 1}
    assert body["facilities"][0]["remainingCapacityKg"] == 2000
    assert body["facilities"][0]["remainingPercent"] == 100.0


def test_dashboard_admin_only(client, citizen_headers):
    assert client.get("/api/v1/dashboard", headers=citizen_headers).status_code == 403


def test_daily_csv_has_one_row_per_stop(client, admin_headers, driver_headers, db_session, citizen, driver):
    add_vehicle(db_session, driver)
    plant = add_facility(db_session)
    for offset in (0.01, 0.02):
        add_request(db_session, citizen, offset)
    route = generate(client, admin_headers).json()["routes"][0]
    first = route["stops"][0]
    client.patch(f"/api/v1/routes/{route['id']}/stops/{first['id']}", json={"status": "COLLECTED"}, headers=driver_headers)

    response = client.get(f"/api/v1/reports/daily.csv?date={DAY}", headers=admin_headers)
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/csv")
    assert f"collection-report-{DAY}.csv" in response.headers["content-disposition"]
    rows = list(csv.reader(io.StringIO(response.content.decode("utf-8"))))
    assert rows[0] == COLUMNS
    assert len(rows) - 1 == len(route["stops"])  # 2 pickups + 1 facility visit
    assert rows[1][1:5] == [str(route["id"]), "KA01AB1234", driver.full_name, str(first["requestId"])]
    assert rows[1][7] == "COLLECTED"
    assert rows[-1][8] == str(plant.id) and rows[-1][4] == ""


def test_other_dates_are_excluded(client, admin_headers, db_session, citizen, driver):
    add_vehicle(db_session, driver)
    add_request(db_session, citizen, 0.01)
    generate(client, admin_headers)
    rows = client.get("/api/v1/reports/daily.csv?date=2026-11-03", headers=admin_headers).text.strip().splitlines()
    assert rows == [",".join(COLUMNS)]


def test_csv_needs_admin_and_date(client, admin_headers, citizen_headers):
    assert client.get(f"/api/v1/reports/daily.csv?date={DAY}", headers=citizen_headers).status_code == 403
    assert client.get("/api/v1/reports/daily.csv", headers=admin_headers).status_code == 422
