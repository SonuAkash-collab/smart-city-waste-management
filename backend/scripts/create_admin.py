"""Create the first Admin account.

Self-registration only makes Citizen accounts, so the first Admin is created
from the command line. Run from the ``backend`` folder:

    python scripts/create_admin.py --email admin@scw.local --password Admin@1234 --name "City Admin"
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import models  # noqa: E402,F401
from app.core.security import hash_password  # noqa: E402
from app.db import Base, SessionLocal, engine  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402
from app.services.auth import get_user_by_email  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an Admin account.")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--name", default="City Admin")
    args = parser.parse_args()

    if len(args.password) < 8:
        print("Password must be at least 8 characters.")
        return 1

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        email = args.email.strip().lower()
        if get_user_by_email(db, email) is not None:
            print(f"An account with {email} already exists.")
            return 1
        db.add(
            User(
                email=email,
                full_name=args.name,
                role=UserRole.ADMIN,
                hashed_password=hash_password(args.password),
                is_active=True,
            )
        )
        db.commit()
    print(f"Admin account created: {email}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
