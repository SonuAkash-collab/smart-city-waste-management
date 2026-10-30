"""Fill the database with demo data for testing and the sprint videos.

Run from the ``backend`` folder:

    python scripts/seed_demo.py --reset

``--reset`` deletes every table first. All demo accounts use the password
``Demo@1234`` except the Admin, which uses ``Admin@1234``.
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import models  # noqa: E402,F401
from app.core.security import hash_password  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.models.collection_request import CollectionRequest, RequestStatus, WasteType  # noqa: E402
from app.models.facility import Facility  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.models.vehicle import Vehicle, VehicleStatus  # noqa: E402
from app.services.requests import initial_priority  # noqa: E402

DEMO_PASSWORD = "Demo@1234"
ADMIN_PASSWORD = "Admin@1234"

USERS = [
    ("admin@scw.local", "City Admin", UserRole.ADMIN),
    ("citizen1@scw.local", "Asha Rao", UserRole.CITIZEN),
    ("citizen2@scw.local", "Kiran Kumar", UserRole.CITIZEN),
    ("driver1@scw.local", "Ravi Shankar", UserRole.DRIVER),
    ("driver2@scw.local", "Meena Gowda", UserRole.DRIVER),
    ("operator1@scw.local", "Prakash Rao", UserRole.OPERATOR),
]

# Depots and facilities around Bengaluru (approximate, for demos only).
VEHICLES = [
    ("KA01AB1234", 1000, ["MIXED", "RECYCLABLE", "GARDEN", "BULKY"], (12.9300, 77.5400), "driver1@scw.local"),
    ("KA01CD5678", 600, ["HAZARDOUS", "MEDICAL", "E_WASTE", "MIXED"], (12.9250, 77.5500), "driver2@scw.local"),
    ("KA05EF9012", 800, ["MIXED", "GARDEN"], (12.9400, 77.5600), None),
]

FACILITIES = [
    ("South Processing Plant", (12.9010, 77.5180), ["MIXED", "GARDEN", "BULKY"], 5000),
    ("City Recycling Centre", (12.9550, 77.5650), ["RECYCLABLE", "MIXED"], 3000),
    ("Hazardous Waste Facility", (12.9150, 77.5900), ["HAZARDOUS", "MEDICAL", "E_WASTE"], 1500),
]

# (citizen, lat, lon, address, waste, kg, status)
REQUESTS = [
    ("citizen1@scw.local", 12.9346, 77.5345, "PES University, Ring Road", "MIXED", 25, RequestStatus.APPROVED),
    ("citizen1@scw.local", 12.9385, 77.5440, "Hosakerehalli Cross", "GARDEN", 60, RequestStatus.APPROVED),
    ("citizen1@scw.local", 12.9290, 77.5470, "Banashankari 3rd Stage", "E_WASTE", 12, RequestStatus.APPROVED),
    ("citizen1@scw.local", 12.9405, 77.5380, "Kathriguppe Main Road", "RECYCLABLE", 30, RequestStatus.SUBMITTED),
    ("citizen2@scw.local", 12.9255, 77.5380, "Uttarahalli Road", "HAZARDOUS", 15, RequestStatus.APPROVED),
    ("citizen2@scw.local", 12.9330, 77.5520, "Kumaraswamy Layout", "BULKY", 120, RequestStatus.APPROVED),
    ("citizen2@scw.local", 12.9440, 77.5470, "Srinivasanagar", "MEDICAL", 8, RequestStatus.APPROVED),
    ("citizen2@scw.local", 12.9210, 77.5300, "Arehalli", "MIXED", 40, RequestStatus.SUBMITTED),
    ("citizen1@scw.local", 12.9360, 77.5600, "Padmanabhanagar", "MIXED", 35, RequestStatus.SUBMITTED),
    ("citizen2@scw.local", 12.9480, 77.5410, "Girinagar", "GARDEN", 50, RequestStatus.SUBMITTED),
]


def seed(reset: bool) -> None:
    if reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(User).count() and not reset:
            print("The database already has data. Run again with --reset to start fresh.")
            return

        users = {}
        for email, name, role in USERS:
            password = ADMIN_PASSWORD if role == UserRole.ADMIN else DEMO_PASSWORD
            user = User(email=email, full_name=name, role=role, hashed_password=hash_password(password))
            db.add(user)
            users[email] = user
        db.flush()

        for reg, capacity, types, depot, driver in VEHICLES:
            db.add(
                Vehicle(
                    registration_number=reg,
                    capacity_kg=capacity,
                    current_load_kg=0,
                    waste_types=types,
                    depot_latitude=depot[0],
                    depot_longitude=depot[1],
                    status=VehicleStatus.AVAILABLE if driver else VehicleStatus.MAINTENANCE,
                    driver_id=users[driver].id if driver else None,
                )
            )

        for name, (lat, lon), types, capacity in FACILITIES:
            db.add(Facility(name=name, latitude=lat, longitude=lon, accepted_waste_types=types, daily_capacity_kg=capacity))

        now = datetime.now(timezone.utc)
        for i, (owner, lat, lon, address, waste, kg, status) in enumerate(REQUESTS):
            created = now - timedelta(hours=3 + i)
            db.add(
                CollectionRequest(
                    citizen_id=users[owner].id,
                    latitude=lat,
                    longitude=lon,
                    address=address,
                    waste_type=WasteType(waste),
                    estimated_quantity_kg=kg,
                    status=status,
                    priority=initial_priority(WasteType(waste)),
                    created_at=created,
                    updated_at=created,
                )
            )
        db.commit()

    print("Demo data ready.")
    print(f"  Admin:     admin@scw.local / {ADMIN_PASSWORD}")
    print(f"  Citizens:  citizen1@scw.local, citizen2@scw.local / {DEMO_PASSWORD}")
    print(f"  Drivers:   driver1@scw.local, driver2@scw.local / {DEMO_PASSWORD}")
    print(f"  Operator:  operator1@scw.local / {DEMO_PASSWORD}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load demo data.")
    parser.add_argument("--reset", action="store_true", help="delete all data first")
    seed(parser.parse_args().reset)
