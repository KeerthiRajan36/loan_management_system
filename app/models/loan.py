from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Enum
)

from sqlalchemy.orm import relationship
from app.database import Base
import enum


class LoanStatus(str, enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    CLOSED = "Closed"


class Loan(Base):

    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )

    loan_type = Column(String(100))

    loan_amount = Column(Float)

    interest_rate = Column(Float)

    tenure_months = Column(Integer)

    approval_status = Column(
        Enum(LoanStatus),
        default=LoanStatus.PENDING
    )

    customer = relationship("Customer")

    emis = relationship(
        "EMI",
        back_populates="loan",
        cascade="all, delete"
    )