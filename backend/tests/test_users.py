"""Tests for Admin account management (TC-ADM-01, SCW-F-003)."""

import pytest

from app.core.security import decode_access_token
from app.models.user import UserRole

from tests.conftest import DEFAULT_PASSWORD


def staff_payload(role="DRIVER", email="driver.new@test.local"):
    return {
        "email": email,
        "fullName": f"New {role.title()}",
        "role": role,
        "temporaryPassword": "Temp@12345",
    }


@pytest.mark.parametrize("role", ["DRIVER", "OPERATOR"])
def test_admin_creates_staff_who_can_log_in(client, admin_headers, role):
    email = f"{role.lower()}.new@test.local"
    created = client.post("/api/v1/users", json=staff_payload(role, email), headers=admin_headers)
    assert created.status_code == 201
    assert created.json()["role"] == role

    login = client.post("/api/v1/auth/login", json={"email": email, "password": "Temp@12345"})
    assert login.status_code == 200
    assert decode_access_token(login.json()["accessToken"])["role"] == role


def test_admin_cannot_create_admin_or_citizen(client, admin_headers):
    for role in ["ADMIN", "CITIZEN"]:
        response = client.post("/api/v1/users", json=staff_payload(role), headers=admin_headers)
        assert response.status_code == 422


def test_duplicate_staff_email(client, admin_headers, driver):
    response = client.post(
        "/api/v1/users", json=staff_payload(email=driver.email), headers=admin_headers
    )
    assert response.status_code == 409


def test_deactivated_staff_cannot_log_in(client, admin_headers, driver, headers_for):
    old_headers = headers_for(driver)
    response = client.patch(
        f"/api/v1/users/{driver.id}/status", json={"isActive": False}, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["isActive"] is False

    login = client.post("/api/v1/auth/login", json={"email": driver.email, "password": DEFAULT_PASSWORD})
    assert login.status_code == 401
    # Tokens issued before deactivation stop working too.
    assert client.get("/api/v1/auth/me", headers=old_headers).status_code == 401


def test_reactivate_account(client, admin_headers, make_user):
    user = make_user(UserRole.OPERATOR, is_active=False)
    response = client.patch(
        f"/api/v1/users/{user.id}/status", json={"isActive": True}, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["isActive"] is True


def test_admin_account_cannot_be_deactivated(client, admin, admin_headers):
    response = client.patch(
        f"/api/v1/users/{admin.id}/status", json={"isActive": False}, headers=admin_headers
    )
    assert response.status_code == 409


def test_unknown_user(client, admin_headers):
    response = client.patch("/api/v1/users/999/status", json={"isActive": False}, headers=admin_headers)
    assert response.status_code == 404


def test_list_users_by_role(client, admin_headers, driver, operator, citizen):
    response = client.get("/api/v1/users?role=DRIVER", headers=admin_headers)
    assert response.status_code == 200
    assert [u["id"] for u in response.json()] == [driver.id]
    everyone = client.get("/api/v1/users", headers=admin_headers).json()
    assert {u["role"] for u in everyone} == {"ADMIN", "DRIVER", "OPERATOR", "CITIZEN"}


def test_non_admin_forbidden(client, citizen_headers, driver_headers):
    for headers in (citizen_headers, driver_headers):
        response = client.post("/api/v1/users", json=staff_payload(), headers=headers)
        assert response.status_code == 403
        assert response.json()["error"]["code"] == "FORBIDDEN"
