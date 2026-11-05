from datetime import date

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.deps import require_roles
from app.db import get_db
from app.models.user import UserRole
from app.services.reports import daily_csv

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(require_roles(UserRole.ADMIN))])


@router.get("/daily.csv")
def daily_report(on_date: date = Query(alias="date"), db: Session = Depends(get_db)):
    """Download the collection report for one date as UTF-8 CSV (SCW-F-052)."""
    return Response(
        content=daily_csv(db, on_date).encode("utf-8"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="collection-report-{on_date}.csv"'},
    )
