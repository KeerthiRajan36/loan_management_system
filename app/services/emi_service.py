from datetime import date

from sqlalchemy.orm import Session

from app.models.loan import Loan, LoanStatus
from app.models.emi import EMI, PaymentStatus

from app.exceptions.custom_exceptions import (
    LoanNotFoundException,
    EMINotFoundException,
    EMIAlreadyPaidException
)

from app.utils.pagination import paginate


class EMIService:

    @staticmethod
    def get_all_emis(
        db: Session,
        page: int = 1,
        limit: int = 10,
        payment_status: str | None = None
    ):

        query = db.query(EMI)

        if payment_status:
            query = query.filter(
                EMI.payment_status == payment_status
            )

        return paginate(
            query=query,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_loan_emis(
        loan_id: int,
        db: Session
    ):

        loan = (
            db.query(Loan)
            .filter(Loan.id == loan_id)
            .first()
        )

        if not loan:
            raise LoanNotFoundException()

        EMIService.update_overdue_status(db)

        return (
            db.query(EMI)
            .filter(EMI.loan_id == loan_id)
            .order_by(EMI.emi_number)
            .all()
        )

    @staticmethod
    def pay_emi(
        emi_id: int,
        db: Session
    ):

        emi = (
            db.query(EMI)
            .filter(EMI.id == emi_id)
            .first()
        )

        if not emi:
            raise EMINotFoundException()

        if emi.payment_status == PaymentStatus.PAID:
            raise EMIAlreadyPaidException()

        emi.payment_status = PaymentStatus.PAID

        db.commit()

        EMIService.close_loan_if_completed(
            db,
            emi.loan_id
        )

        db.refresh(emi)

        return {
            "message": "EMI paid successfully",
            "emi": emi
        }

    @staticmethod
    def update_overdue_status(
        db: Session
    ):

        today = date.today()

        overdue_emis = (
            db.query(EMI)
            .filter(
                EMI.payment_status == PaymentStatus.PENDING,
                EMI.due_date < today
            )
            .all()
        )

        for emi in overdue_emis:

            emi.payment_status = PaymentStatus.OVERDUE

        db.commit()

    @staticmethod
    def close_loan_if_completed(
        db: Session,
        loan_id: int
    ):

        loan = (
            db.query(Loan)
            .filter(Loan.id == loan_id)
            .first()
        )

        if not loan:
            return

        pending = (
            db.query(EMI)
            .filter(
                EMI.loan_id == loan_id,
                EMI.payment_status != PaymentStatus.PAID
            )
            .count()
        )

        if pending == 0:

            loan.approval_status = LoanStatus.CLOSED

            db.commit()