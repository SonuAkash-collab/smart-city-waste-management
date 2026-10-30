from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.core.errors import register_error_handlers
from app.db import Base, engine
from app.routers import (
    audit,
    auth,
    dashboard,
    facilities,
    geo,
    notifications,
    reports,
    requests,
    routes,
    security,
    users,
    vehicles,
)

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Smart City Waste Management System", version="1.0", lifespan=lifespan)
register_error_handlers(app)

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(users.router, prefix=API_PREFIX)
app.include_router(notifications.router, prefix=API_PREFIX)
app.include_router(reports.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(requests.router, prefix=API_PREFIX)
app.include_router(routes.router, prefix=API_PREFIX)
app.include_router(geo.router, prefix=API_PREFIX)
app.include_router(vehicles.router, prefix=API_PREFIX)
app.include_router(facilities.router, prefix=API_PREFIX)
app.include_router(audit.router, prefix=API_PREFIX)
app.include_router(security.router, prefix=API_PREFIX)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


# The web app (frontend/) is served from the same server, so one command runs
# everything. It is mounted last so the API routes above take priority.
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="web")
