"""Seed data for performance tests (TC-PERF-01/02): 200 approved requests, 20 vehicles,
5 facilities, 20 citizens and one admin, all with password Perf@1234.

    python scripts/seed_perf.py        (uses DATABASE_URL, default sqlite:///./app.db; deletes all data first)
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import models  # noqa: E402,F401
from app.core.security import hash_password  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.models.collection_request import CollectionRequest, RequestStatus, WasteType  # noqa: E402
from app.models.facility import Facility  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.models.vehicle import Vehicle  # noqa: E402
from app.services.requests import initial_priority  # noqa: E402

PASSWORD = "Perf@1234"
TYPES = list(WasteType)


def main() -> None:
    rng = random.Random(7)
    spot = lambda: (12.9716 + rng.uniform(-0.15, 0.15), 77.5946 + rng.uniform(-0.15, 0.15))  # noqa: E731
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    hashed = hash_password(PASSWORD)
    with SessionLocal() as db:
        db.add(User(email="perf.admin@scw.local", full_name="Perf Admin", role=UserRole.ADMIN, hashed_password=hashed))
        citizens = [User(email=f"perf.citizen{i}@scw.local", full_name=f"Citizen {i}", role=UserRole.CITIZEN, hashed_password=hashed) for i in range(1, 21)]
        drivers = [User(email=f"perf.driver{i}@scw.local", full_name=f"Driver {i}", role=UserRole.DRIVER, hashed_password=hashed) for i in range(1, 21)]
        db.add_all(citizens + drivers)
        db.flush()
        for i, driver in enumerate(drivers, start=1):
            lat, lon = spot()
            db.add(Vehicle(registration_number=f"KA99PF{i:04d}", capacity_kg=rng.choice([500, 800, 1000]), current_load_kg=0,
                           waste_types=[t.value for t in TYPES], depot_latitude=lat, depot_longitude=lon, driver_id=driver.id))
        for i in range(1, 6):
            lat, lon = spot()
            db.add(Facility(name=f"Perf Facility {i}", latitude=lat, longitude=lon, accepted_waste_types=[t.value for t in TYPES], daily_capacity_kg=50_000))
        for _ in range(200):
            lat, lon = spot()
            waste = rng.choice(TYPES)
            db.add(CollectionRequest(citizen_id=rng.choice(citizens).id, latitude=lat, longitude=lon, waste_type=waste,
                                     estimated_quantity_kg=round(rng.uniform(5, 80), 1), status=RequestStatus.APPROVED,
                                     priority=initial_priority(waste)))
        db.commit()
    print("Perf data ready: 200 approved requests, 20 vehicles with drivers, 5 facilities.")


if __name__ == "__main__":
    main()
