"""Tests for HTTPS redirect and security headers (TC-SEC-02 part C, TC-SEC-03)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.transport import apply_transport_security


def make_app(force_https):
    app = FastAPI()

    @app.get("/api/v1/vehicles")
    def protected():
        return {"secret": "data"}

    apply_transport_security(app, force_https=force_https)
    return app


def test_plain_http_redirected_without_data():
    client = TestClient(make_app(True), base_url="http://testserver")
    response = client.get("/api/v1/vehicles", follow_redirects=False)
    assert response.status_code in (307, 308)
    assert response.headers["location"].startswith("https://")
    assert "secret" not in response.text


def test_https_request_served_with_hsts():
    client = TestClient(make_app(True), base_url="https://testserver")
    response = client.get("/api/v1/vehicles")
    assert response.status_code == 200
    assert "max-age" in response.headers["strict-transport-security"]


def test_security_headers_always_present(client):
    response = client.get("/health")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
