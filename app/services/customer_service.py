from sqlalchemy.orm import Session

from app.models.customer import Customer

from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate
)

from app.exceptions.custom_exceptions import (
    CustomerNotFoundException,
    EmailAlreadyExistsException
)

from app.utils.pagination import paginate


class CustomerService:

    @staticmethod
    def create_customer(
        db: Session,
        request: CustomerCreate
    ):

        existing = (
            db.query(Customer)
            .filter(Customer.email == request.email)
            .first()
        )

        if existing:
            raise EmailAlreadyExistsException()

        customer = Customer(
            name=request.name,
            email=request.email,
            phone=request.phone,
            address=request.address,
            credit_score=request.credit_score
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def get_all_customers(
        db: Session,
        page: int = 1,
        limit: int = 10
    ):

        query = db.query(Customer)

        return paginate(
            query=query,
            page=page,
            limit=limit
        )

    @staticmethod
    def get_customer(
        customer_id: int,
        db: Session
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise CustomerNotFoundException()

        return customer

    @staticmethod
    def update_customer(
        customer_id: int,
        request: CustomerUpdate,
        db: Session
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise CustomerNotFoundException()

        update_data = request.model_dump(exclude_unset=True)

        if "email" in update_data:

            existing = (
                db.query(Customer)
                .filter(
                    Customer.email == update_data["email"],
                    Customer.id != customer_id
                )
                .first()
            )

            if existing:
                raise EmailAlreadyExistsException()

        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def delete_customer(
        customer_id: int,
        db: Session
    ):

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise CustomerNotFoundException()

        db.delete(customer)
        db.commit()

        return {
            "message": "Customer deleted successfully"
        }