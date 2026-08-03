from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.loan import (
    LoanCreate,
    LoanUpdate,
    LoanResponse
)

from app.services.loan_service import LoanService

from app.utils.roles import role_required

router = APIRouter(
    prefix="/loans",
    tags=["Loans"]
)


@router.post(
    "",
    response_model=LoanResponse,
    status_code=201
)
def create_loan(
    request: LoanCreate,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return LoanService.create_loan(
        db,
        request
    )


@router.get("")
def get_loans(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return LoanService.get_loans(
        db=db,
        page=page,
        limit=limit
    )


@router.get(
    "/search"
)
def search_loans(
    customer_name: Optional[str] = None,
    loan_type: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return LoanService.search_loans(
        db=db,
        customer_name=customer_name,
        loan_type=loan_type,
        page=page,
        limit=limit
    )


@router.get(
    "/{loan_id}",
    response_model=LoanResponse
)
def get_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer", "Customer"]
        )
    )
):
    return LoanService.get_loan(
        loan_id,
        db
    )


@router.put(
    "/{loan_id}",
    response_model=LoanResponse
)
def update_loan(
    loan_id: int,
    request: LoanUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return LoanService.update_loan(
        loan_id,
        request,
        db
    )