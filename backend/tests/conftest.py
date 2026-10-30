import itertools
import os

os.environ.setdefault("BCRYPT_ROUNDS", "4")  # fast hashing in tests only

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app import models  # noqa: F401,E402
from app.core.security import create_access_token, hash_password  # noqa: E402
from app.db import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User, UserRole  # noqa: E402

DEFAULT_PASSWORD = "Passw0rd!"


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(bind=engine, autocommit=False, autoflush=False)()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def make_user(db_session):
    """Create a user directly in the test database."""
    counter = itertools.count(1)

    def _make(
        role: UserRole = UserRole.CITIZEN,
        email: str | None = None,
        password: str = DEFAULT_PASSWORD,
        full_name: str | None = None,
        is_active: bool = True,
    ) -> User:
        number = next(counter)
        user = User(
            email=email or f"{role.value.lower()}{number}@test.local",
            hashed_password=hash_password(password),
            full_name=full_name or f"{role.value.title()} {number}",
            role=role,
            is_active=is_active,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _make


@pytest.fixture
def headers_for():
    """Return Authorization headers for a user."""

    def _headers(user: User) -> dict[str, str]:
        token = create_access_token(user.id, user.role.value)
        return {"Authorization": f"Bearer {token}"}

    return _headers


@pytest.fixture
def admin(make_user):
    return make_user(UserRole.ADMIN)


@pytest.fixture
def citizen(make_user):
    return make_user(UserRole.CITIZEN)


@pytest.fixture
def driver(make_user):
    return make_user(UserRole.DRIVER)


@pytest.fixture
def operator(make_user):
    return make_user(UserRole.OPERATOR)


@pytest.fixture
def admin_headers(admin, headers_for):
    return headers_for(admin)


@pytest.fixture
def citizen_headers(citizen, headers_for):
    return headers_for(citizen)


@pytest.fixture
def driver_headers(driver, headers_for):
    return headers_for(driver)


@pytest.fixture
def operator_headers(operator, headers_for):
    return headers_for(operator)
