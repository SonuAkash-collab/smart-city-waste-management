"""The web app is served by FastAPI next to the API."""


def test_index_page_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Smart City Waste" in response.text
    assert "src/app.js" in response.text


def test_static_files_served(client):
    assert client.get("/src/app.js").status_code == 200
    assert client.get("/vendor/leaflet/leaflet.css").status_code == 200


def test_unknown_api_path_gives_json_error(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_api_docs_still_available(client):
    assert client.get("/docs").status_code == 200
    assert client.get("/health").json() == {"status": "ok"}
