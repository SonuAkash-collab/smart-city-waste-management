"""Tests for registration, login, tokens and role checks.

Covers TC-AUTH-01, TC-AUTH-02 (server side) and TC-SEC-02 parts A and B.
"""

from datetime import datetime, timedelta, timezone

import pytest
from fastapi import APIRouter, Depends
from jose import jwt

from app.core import config
from app.core.deps import require_roles
from app.core.security import create_access_token, decode_access_token
from app.main import app
from app.models.user import User, UserRole

from tests.conftest import DEFAULT_PASSWORD

# A tiny admin-only endpoint so the role guard can be tested on its own.
_probe = APIRouter()


@_probe.get("/_test/admin-only")
def _admin_only(user: User = Depends(require_roles(UserRole.ADMIN))):
    return {"ok": True, "userId": user.id}


app.include_router(_probe)


def login(client, email, password=DEFAULT_PASSWORD):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


# --- registration -----------------------------------------------------------


def test_register_creates_citizen(client, db_session):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": " New@Test.Local ", "password": "Secret123!", "fullName": "New Citizen"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "new@test.local"
    assert body["role"] == "CITIZEN"
    stored = db_session.get(User, body["id"])
    assert stored.hashed_password.startswith("$2")  # bcrypt, not plain text
    assert stored.hashed_password != "Secret123!"


def test_register_cannot_choose_role(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "x@test.local", "password": "Secret123!", "fullName": "X", "role": "ADMIN"},
    )
    assert response.status_code == 201
    assert response.json()["role"] == "CITIZEN"


def test_register_duplicate_email_conflict(client, citizen):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": citizen.email.upper(), "password": "Secret123!", "fullName": "Dup"},
    )
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "EMAIL_TAKEN"


@pytest.mark.parametrize(
    "payload",
    [
        {"email": "bad-email", "password": "Secret123!", "fullName": "A"},
        {"email": "a@test.local", "password": "short", "fullName": "A"},
        {"email": "a@test.local", "password": "Secret123!", "fullName": "  "},
    ],
)
def test_register_validation(client, payload):
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


# --- login (TC-AUTH-01) -----------------------------------------------------


@pytest.mark.parametrize("role", list(UserRole))
def test_login_returns_token_with_role(client, make_user, role):
    user = make_user(role)
    response = login(client, user.email)
    assert response.status_code == 200
    body = response.json()
    claims = decode_access_token(body["accessToken"])
    assert claims["role"] == role.value
    assert claims["sub"] == str(user.id)
    assert claims["exp"] - claims["iat"] == 30 * 60  # SCW-SEC-002
    assert body["user"]["role"] == role.value


def test_login_wrong_password(client, citizen):
    response = login(client, citizen.email, "Wrong@123")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"
    assert "accessToken" not in response.json()


def test_login_unknown_email_same_error(client):
    response = login(client, "nobody@test.local", "Wrong@123")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"


def test_login_empty_email_is_validation_error(client):
    response = client.post("/api/v1/auth/login", json={"email": "", "password": "x"})
    assert response.status_code == 422


def test_login_deactivated_account(client, make_user):
    user = make_user(UserRole.DRIVER, is_active=False)
    response = login(client, user.email)
    assert response.status_code == 401


# --- tokens (TC-SEC-02 part A) ----------------------------------------------


def test_me_with_valid_token(client, citizen, citizen_headers):
    response = client.get("/api/v1/auth/me", headers=citizen_headers)
    assert response.status_code == 200
    assert response.json()["email"] == citizen.email


def test_missing_token_rejected(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "NOT_AUTHENTICATED"


def test_expired_token_rejected(client, citizen):
    old = datetime.now(timezone.utc) - timedelta(minutes=31)
    token = create_access_token(citizen.id, citizen.role.value, now=old)
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "TOKEN_EXPIRED"


def test_forged_token_rejected(client, citizen):
    forged = jwt.encode(
        {"sub": str(citizen.id), "role": "ADMIN", "exp": 9999999999},
        "not-the-real-secret",
        algorithm=config.JWT_ALGORITHM,
    )
    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {forged}"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "INVALID_TOKEN"


def test_malformed_token_rejected(client):
    response = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer abc.def"})
    assert response.status_code == 401


def test_token_of_deactivated_user_rejected(client, citizen, citizen_headers, db_session):
    citizen.is_active = False
    db_session.commit()
    response = client.get("/api/v1/auth/me", headers=citizen_headers)
    assert response.status_code == 401


# --- role guard (TC-AUTH-02, TC-SEC-02 part B) -------------------------------


def test_admin_allowed_on_admin_endpoint(client, admin_headers):
    response = client.get("/_test/admin-only", headers=admin_headers)
    assert response.status_code == 200


@pytest.mark.parametrize("role", [UserRole.CITIZEN, UserRole.DRIVER, UserRole.OPERATOR])
def test_other_roles_forbidden_on_admin_endpoint(client, make_user, headers_for, role):
    response = client.get("/_test/admin-only", headers=headers_for(make_user(role)))
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "FORBIDDEN"


def test_role_comes_from_database_not_token(client, citizen):
    # A token that claims ADMIN for a citizen account still gets 403,
    # because the server reads the role from the database.
    token = create_access_token(citizen.id, "ADMIN")
    response = client.get("/_test/admin-only", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
