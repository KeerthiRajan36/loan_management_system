from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse
)

from app.schemas.common import MessageResponse

from app.services.customer_service import CustomerService

from app.utils.roles import role_required

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=201
)
def create_customer(
    request: CustomerCreate,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return CustomerService.create_customer(
        db,
        request
    )


@router.get("")
def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return CustomerService.get_all_customers(
        db=db,
        page=page,
        limit=limit
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return CustomerService.get_customer(
        customer_id,
        db
    )


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    request: CustomerUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin", "Loan Officer"]
        )
    )
):
    return CustomerService.update_customer(
        customer_id,
        request,
        db
    )


@router.delete(
    "/{customer_id}",
    response_model=MessageResponse
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        role_required(
            ["Admin"]
        )
    )
):
    return CustomerService.delete_customer(
        customer_id,
        db
    )