from datetime import date

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.loan import Loan, LoanStatus
from app.models.customer import Customer
from app.models.emi import EMI, PaymentStatus

from app.schemas.loan import LoanCreate, LoanUpdate

from app.exceptions.custom_exceptions import (
    LoanNotFoundException,
    CustomerNotFoundException,
    CustomerNotEligibleException,
    LoanAlreadyApprovedException,
    LoanAlreadyRejectedException,
)

from app.utils.pagination import paginate


class LoanService:

    MINIMUM_CREDIT_SCORE = 650

    @staticmethod
    def create_loan(
        db: Session,
        request: LoanCreate
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == request.customer_id)
            .first()
        )

        if not customer:
            raise CustomerNotFoundException()

        loan = Loan(
            customer_id=request.customer_id,
            loan_type=request.loan_type,
            loan_amount=request.loan_amount,
            interest_rate=request.interest_rate,
            tenure_months=request.tenure_months,
            approval_status=LoanStatus.PENDING
        )

        db.add(loan)
        db.commit()
        db.refresh(loan)

        return loan

    @staticmethod
    def get_loans(
        db: Session,
        page=1,
        limit=10
    ):

        query = db.query(Loan)

        return paginate(query, page, limit)

    @staticmethod
    def get_loan(
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

        return loan

    @staticmethod
    def search_loans(
        db: Session,
        customer_name=None,
        loan_type=None,
        page=1,
        limit=10
    ):

        query = (
            db.query(Loan)
            .join(Customer)
        )

        if customer_name:

            query = query.filter(
                Customer.name.ilike(f"%{customer_name}%")
            )

        if loan_type:

            query = query.filter(
                Loan.loan_type.ilike(f"%{loan_type}%")
            )

        return paginate(query, page, limit)

    @staticmethod
    def update_loan(
        loan_id: int,
        request: LoanUpdate,
        db: Session
    ):

        loan = (
            db.query(Loan)
            .filter(Loan.id == loan_id)
            .first()
        )

        if not loan:
            raise LoanNotFoundException()

        if loan.approval_status == LoanStatus.APPROVED:
            raise LoanAlreadyApprovedException()

        if loan.approval_status == LoanStatus.REJECTED:
            raise LoanAlreadyRejectedException()

        customer = (
            db.query(Customer)
            .filter(Customer.id == loan.customer_id)
            .first()
        )

        if request.approval_status == LoanStatus.APPROVED:

            if customer.credit_score < LoanService.MINIMUM_CREDIT_SCORE:
                raise CustomerNotEligibleException()

            loan.approval_status = LoanStatus.APPROVED

            LoanService.generate_emi_schedule(
                db,
                loan
            )

        elif request.approval_status == LoanStatus.REJECTED:

            loan.approval_status = LoanStatus.REJECTED

        db.commit()
        db.refresh(loan)

        return loan

    @staticmethod
    def generate_emi_schedule(
        db: Session,
        loan: Loan
    ):

        principal = loan.loan_amount

        interest = (
            principal *
            loan.interest_rate *
            loan.tenure_months
        ) / (100 * 12)

        total = principal + interest

        emi_amount = round(
            total / loan.tenure_months,
            2
        )

        current_date = date.today()

        for emi_no in range(
            1,
            loan.tenure_months + 1
        ):

            emi = EMI(

                loan_id=loan.id,

                emi_number=emi_no,

                due_date=current_date +
                relativedelta(months=emi_no),

                amount=emi_amount,

                payment_status=PaymentStatus.PENDING

            )

            db.add(emi)

        db.commit()