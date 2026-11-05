"""Tests for bcrypt storage and account lockout (TC-SEC-01)."""

from datetime import datetime, timedelta, timezone

from tests.conftest import DEFAULT_PASSWORD


def login(client, user, password):
    return client.post("/api/v1/auth/login", json={"email": user.email, "password": password})


def fail(client, user, times):
    return [login(client, user, "WrongPass!123").status_code for _ in range(times)]


def test_password_stored_as_bcrypt_hash(citizen):
    assert citizen.hashed_password.startswith("$2b$")
    assert DEFAULT_PASSWORD not in citizen.hashed_password


def test_four_failures_do_not_lock(client, citizen):
    assert fail(client, citizen, 4) == [401] * 4
    assert login(client, citizen, DEFAULT_PASSWORD).status_code == 200


def test_fifth_failure_locks_for_15_minutes(client, citizen, db_session):
    assert fail(client, citizen, 5) == [401, 401, 401, 401, 403]
    response = login(client, citizen, DEFAULT_PASSWORD)
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ACCOUNT_LOCKED"
    db_session.refresh(citizen)
    left = citizen.locked_until.replace(tzinfo=timezone.utc) - datetime.now(timezone.utc)
    assert timedelta(minutes=14) < left <= timedelta(minutes=15)


def test_login_works_after_lock_expires(client, citizen, db_session):
    fail(client, citizen, 5)
    citizen.locked_until = datetime.now(timezone.utc) - timedelta(seconds=1)
    db_session.commit()
    assert login(client, citizen, DEFAULT_PASSWORD).status_code == 200


def test_success_resets_counter(client, citizen):
    fail(client, citizen, 4)
    assert login(client, citizen, DEFAULT_PASSWORD).status_code == 200
    assert fail(client, citizen, 4) == [401] * 4  # counter started again from zero
    assert login(client, citizen, DEFAULT_PASSWORD).status_code == 200


def test_unknown_email_never_locks_anything(client):
    response = client.post("/api/v1/auth/login", json={"email": "ghost@test.local", "password": "x"})
    assert response.status_code == 401
