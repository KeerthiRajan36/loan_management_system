from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.emi_service import EMIService
from app.utils.roles import role_required
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/emis",
    tags=["EMI Management"]
)


@router.get("")
def get_all_emis(
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

    return EMIService.get_all_emis(
        db=db,
        payment_status=payment_status,
        page=page,
        limit=limit
    )


@router.get("/loan/{loan_id}")
def get_loan_emis(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return EMIService.get_loan_emis(
        loan_id=loan_id,
        db=db,
        current_user=current_user
    )


@router.put("/{emi_id}/pay")
def pay_emi(
    emi_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        role_required(
            ["Customer"]
        )
    )
):

    return EMIService.pay_emi(
        emi_id=emi_id,
        db=db,
        current_user=current_user
    )