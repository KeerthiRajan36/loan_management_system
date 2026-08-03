from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    phone = Column(String(20))

    address = Column(String(250))

    credit_score = Column(Float)