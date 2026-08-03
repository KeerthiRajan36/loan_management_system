from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import *


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(CustomerNotFoundException)
    async def customer_not_found(request: Request, exc: CustomerNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Customer not found"
            }
        )

    @app.exception_handler(LoanNotFoundException)
    async def loan_not_found(request: Request, exc: LoanNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "Loan not found"
            }
        )

    @app.exception_handler(EMINotFoundException)
    async def emi_not_found(request: Request, exc: EMINotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "EMI not found"
            }
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found(request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "message": "User not found"
            }
        )

    @app.exception_handler(EmailAlreadyExistsException)
    async def email_exists(request: Request, exc: EmailAlreadyExistsException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Email already exists"
            }
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Invalid email or password"
            }
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized(request: Request, exc: UnauthorizedException):
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Authentication required"
            }
        )

    @app.exception_handler(ForbiddenException)
    async def forbidden(request: Request, exc: ForbiddenException):
        return JSONResponse(
            status_code=403,
            content={
                "success": False,
                "message": "Permission denied"
            }
        )

    @app.exception_handler(CustomerNotEligibleException)
    async def customer_not_eligible(request: Request, exc: CustomerNotEligibleException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Customer is not eligible for loan approval"
            }
        )

    @app.exception_handler(LoanAlreadyApprovedException)
    async def loan_already_approved(request: Request, exc: LoanAlreadyApprovedException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Loan is already approved"
            }
        )

    @app.exception_handler(LoanAlreadyRejectedException)
    async def loan_already_rejected(request: Request, exc: LoanAlreadyRejectedException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Loan is already rejected"
            }
        )

    @app.exception_handler(LoanAlreadyClosedException)
    async def loan_already_closed(request: Request, exc: LoanAlreadyClosedException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Loan is already closed"
            }
        )

    @app.exception_handler(EMIAlreadyPaidException)
    async def emi_already_paid(request: Request, exc: EMIAlreadyPaidException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "This EMI has already been paid"
            }
        )

    @app.exception_handler(InvalidLoanAmountException)
    async def invalid_loan_amount(request: Request, exc: InvalidLoanAmountException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Loan amount must be greater than zero"
            }
        )

    @app.exception_handler(InvalidEMIAmountException)
    async def invalid_emi_amount(request: Request, exc: InvalidEMIAmountException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "EMI amount must be greater than zero"
            }
        )

    @app.exception_handler(InvalidCreditScoreException)
    async def invalid_credit_score(request: Request, exc: InvalidCreditScoreException):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Invalid credit score"
            }
        )