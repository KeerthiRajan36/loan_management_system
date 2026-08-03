from pydantic import BaseModel, Field
from enum import Enum


class LoanStatus(str, Enum):
    Pending = "Pending"
    Approved = "Approved"
    Rejected = "Rejected"
    Closed = "Closed"


class LoanCreate(BaseModel):
    customer_id: int
    loan_type: str
    loan_amount: float = Field(..., gt=0)
    interest_rate: float = Field(..., gt=0)
    tenure_months: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": 1,
                "loan_type": "Home Loan",
                "loan_amount": 1000000,
                "interest_rate": 8.5,
                "tenure_months": 120
            }
        }


class LoanUpdate(BaseModel):
    approval_status: LoanStatus


class LoanResponse(BaseModel):
    id: int
    customer_id: int
    loan_type: str
    loan_amount: float
    interest_rate: float
    tenure_months: int
    approval_status: LoanStatus

    class Config:
        from_attributes = True