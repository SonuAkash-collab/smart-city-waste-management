"""Locust load test for SCW-NF-002 / TC-PERF-02: 95% of calls under 2 s at 100 users.

Run against a server seeded with scripts/seed_perf.py, for example:
    locust -f tests/perf/locustfile.py --headless -u 100 -r 10 -t 60s --host http://localhost:8000
or simply:  python scripts/run_perf.py
"""

import random

from locust import HttpUser, between, task

CITIZENS = [f"perf.citizen{i}@scw.local" for i in range(1, 21)]
PASSWORD = "Perf@1234"


class CitizenUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        email = random.choice(CITIZENS)
        token = self.client.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD}).json()["accessToken"]
        self.client.headers["Authorization"] = f"Bearer {token}"

    @task(3)
    def list_my_requests(self):
        self.client.get("/api/v1/requests?page=1&size=10", name="GET /requests")

    @task(1)
    def submit_request(self):
        self.client.post(
            "/api/v1/requests",
            json={"latitude": 12.93 + random.random() / 50, "longitude": 77.54 + random.random() / 50,
                  "wasteType": random.choice(["MIXED", "GARDEN", "RECYCLABLE"]), "estimatedQuantityKg": 15},
            name="POST /requests",
        )

    @task(2)
    def notifications(self):
        self.client.get("/api/v1/notifications", name="GET /notifications")


class AdminUser(HttpUser):
    wait_time = between(2, 5)
    weight = 1

    def on_start(self):
        token = self.client.post("/api/v1/auth/login", json={"email": "perf.admin@scw.local", "password": PASSWORD}).json()["accessToken"]
        self.client.headers["Authorization"] = f"Bearer {token}"

    @task(2)
    def dashboard(self):
        self.client.get("/api/v1/dashboard", name="GET /dashboard")

    @task(2)
    def filter_requests(self):
        self.client.get("/api/v1/requests?status=APPROVED&page=1&size=20", name="GET /requests (admin filter)")
