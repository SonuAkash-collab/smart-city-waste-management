"""SCW-NF-001: plan 200 requests for 20 vehicles in under 10 seconds (TC-PERF-01 step 3)."""

import random
import time

from app.services.route_engine import FacilityInput, RequestInput, VehicleInput, plan_routes

WASTE_TYPES = ["HAZARDOUS", "MEDICAL", "E_WASTE", "MIXED", "RECYCLABLE", "GARDEN", "BULKY"]
PRIORITY = {"HAZARDOUS": "HIGH", "MEDICAL": "HIGH", "E_WASTE": "HIGH", "MIXED": "MEDIUM",
            "RECYCLABLE": "MEDIUM", "GARDEN": "LOW", "BULKY": "LOW"}


def build_city(seed=42):
    rng = random.Random(seed)
    center = (12.9716, 77.5946)  # Bengaluru

    def spot():
        return center[0] + rng.uniform(-0.15, 0.15), center[1] + rng.uniform(-0.15, 0.15)

    requests = []
    for i in range(1, 201):
        lat, lon = spot()
        waste = rng.choice(WASTE_TYPES)
        requests.append(RequestInput(i, lat, lon, waste, rng.uniform(5, 80), PRIORITY[waste]))
    vehicles = []
    for i in range(1, 21):
        lat, lon = spot()
        vehicles.append(VehicleInput(i, rng.choice([500.0, 800.0, 1000.0]), tuple(WASTE_TYPES), lat, lon))
    facilities = []
    for i in range(1, 6):
        lat, lon = spot()
        facilities.append(FacilityInput(i, lat, lon, tuple(WASTE_TYPES), 50_000.0))
    return requests, vehicles, facilities


def test_200_requests_20_vehicles_under_10_seconds():
    requests, vehicles, facilities = build_city()
    started = time.perf_counter()
    plan = plan_routes(requests, vehicles, facilities)
    elapsed = time.perf_counter() - started

    planned = [s.request_id for r in plan.routes for s in r.stops if s.request_id is not None]
    assert sorted(planned) == list(range(1, 201))
    assert plan.unassigned == []
    assert elapsed < 10.0, f"route planning took {elapsed:.2f} s"
    print(f"\nSCW-NF-001: planned 200 requests / 20 vehicles in {elapsed:.3f} s")
