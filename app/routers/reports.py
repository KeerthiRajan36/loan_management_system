from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.report_service import ReportService

from app.utils.roles import role_required

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return ReportService.dashboard(db)


@router.get("/search-loans")
def search_loans(
    customer_name: Optional[str] = None,
    loan_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):

    return ReportService.search_loans(
        db=db,
        customer_name=customer_name,
        loan_type=loan_type,
        page=page,
        limit=limit
    )


@router.get("/filter-emis")
def filter_emis(
    payment_status: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):

    return ReportService.filter_emis(
        db=db,
        payment_status=payment_status,
        page=page,
        limit=limit
    )


@router.get("/overdue-emis")
def overdue_report(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):

    return ReportService.overdue_report(
        db=db,
        page=page,
        limit=limit
    )