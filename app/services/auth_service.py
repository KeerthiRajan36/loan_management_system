from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.schemas.auth import LoginRequest

from app.utils.hashing import hash_password
from app.utils.hashing import verify_password
from app.utils.jwt import create_access_token

from app.exceptions.custom_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException
)


class AuthService:

    @staticmethod
    def register(db: Session, request: RegisterRequest):

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise EmailAlreadyExistsException()

        new_user = User(
            username=request.username,
            email=request.email,
            hashed_password=hash_password(request.password),
            role=request.role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully"
        }

    @staticmethod
    def login(db: Session, request: LoginRequest):

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(
            request.password,
            user.hashed_password
        ):
            raise InvalidCredentialsException()

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role.value
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }