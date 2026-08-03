from sqlalchemy import (
    Column,
    Integer,
    Float,
    Date,
    ForeignKey,
    Enum
)

from sqlalchemy.orm import relationship

from app.database import Base

import enum


class PaymentStatus(str, enum.Enum):
    PENDING = "Pending"
    PAID = "Paid"
    OVERDUE = "Overdue"


class EMI(Base):

    __tablename__ = "emis"

    id = Column(Integer, primary_key=True, index=True)

    loan_id = Column(
        Integer,
        ForeignKey("loans.id")
    )

    emi_number = Column(Integer)

    due_date = Column(Date)

    amount = Column(Float)

    payment_status = Column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING
    )

    loan = relationship(
        "Loan",
        back_populates="emis"
    )