from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class PaymentStatus(str, Enum):
    Pending = "Pending"
    Paid = "Paid"
    Overdue = "Overdue"


class EMICreate(BaseModel):
    loan_id: int
    emi_number: int
    due_date: date
    amount: float = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "loan_id": 1,
                "emi_number": 1,
                "due_date": "2026-09-01",
                "amount": 9500
            }
        }


class EMIPayment(BaseModel):
    payment_status: PaymentStatus = PaymentStatus.Paid


class EMIResponse(BaseModel):
    id: int
    loan_id: int
    emi_number: int
    due_date: date
    amount: float
    payment_status: PaymentStatus

    class Config:
        from_attributes = True