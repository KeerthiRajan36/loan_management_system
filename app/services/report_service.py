from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.customer import Customer
from app.models.loan import Loan, LoanStatus
from app.models.emi import EMI, PaymentStatus

from app.utils.pagination import paginate


class ReportService:

    @staticmethod
    def search_loans(
        db: Session,
        customer_name: str = None,
        loan_type: str = None,
        page: int = 1,
        limit: int = 10
    ):

        query = (
            db.query(Loan)
            .join(Customer)
        )

        if customer_name:

            query = query.filter(
                Customer.name.ilike(
                    f"%{customer_name}%"
                )
            )

        if loan_type:

            query = query.filter(
                Loan.loan_type.ilike(
                    f"%{loan_type}%"
                )
            )

        return paginate(
            query=query,
            page=page,
            limit=limit
        )

    @staticmethod
    def filter_emis(
        db: Session,
        payment_status: str,
        page: int = 1,
        limit: int = 10
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
    def overdue_report(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        today = date.today()

        overdue = (
            db.query(EMI)
            .filter(
                EMI.due_date < today,
                EMI.payment_status != PaymentStatus.PAID
            )
        )

        return paginate(
            query=overdue,
            page=page,
            limit=limit
        )

    @staticmethod
    def dashboard(db: Session):

        total_customers = (
            db.query(Customer)
            .count()
        )

        total_loans = (
            db.query(Loan)
            .count()
        )

        approved_loans = (
            db.query(Loan)
            .filter(
                Loan.approval_status == LoanStatus.APPROVED
            )
            .count()
        )

        pending_loans = (
            db.query(Loan)
            .filter(
                Loan.approval_status == LoanStatus.PENDING
            )
            .count()
        )

        rejected_loans = (
            db.query(Loan)
            .filter(
                Loan.approval_status == LoanStatus.REJECTED
            )
            .count()
        )

        closed_loans = (
            db.query(Loan)
            .filter(
                Loan.approval_status == LoanStatus.CLOSED
            )
            .count()
        )

        total_loan_amount = (
            db.query(
                func.sum(
                    Loan.loan_amount
                )
            )
            .scalar() or 0
        )

        total_emis = (
            db.query(EMI)
            .count()
        )

        pending_emis = (
            db.query(EMI)
            .filter(
                EMI.payment_status == PaymentStatus.PENDING
            )
            .count()
        )

        paid_emis = (
            db.query(EMI)
            .filter(
                EMI.payment_status == PaymentStatus.PAID
            )
            .count()
        )

        overdue_emis = (
            db.query(EMI)
            .filter(
                EMI.payment_status == PaymentStatus.OVERDUE
            )
            .count()
        )

        return {

            "customers": total_customers,

            "loans": total_loans,

            "approved_loans": approved_loans,

            "pending_loans": pending_loans,

            "rejected_loans": rejected_loans,

            "closed_loans": closed_loans,

            "total_loan_amount": total_loan_amount,

            "total_emis": total_emis,

            "pending_emis": pending_emis,

            "paid_emis": paid_emis,

            "overdue_emis": overdue_emis

        }