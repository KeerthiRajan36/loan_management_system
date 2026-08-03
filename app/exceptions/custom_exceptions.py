class CustomerNotFoundException(Exception):
    pass


class LoanNotFoundException(Exception):
    pass


class EMINotFoundException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class EmailAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class LoanAlreadyApprovedException(Exception):
    pass


class LoanAlreadyRejectedException(Exception):
    pass


class CustomerNotEligibleException(Exception):
    pass


class LoanAlreadyClosedException(Exception):
    pass


class EMIAlreadyPaidException(Exception):
    pass


class InvalidLoanAmountException(Exception):
    pass


class InvalidEMIAmountException(Exception):
    pass


class InvalidCreditScoreException(Exception):
    pass