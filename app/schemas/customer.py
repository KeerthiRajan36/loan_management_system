from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str
    address: str
    credit_score: float = Field(..., ge=300, le=900)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "john@gmail.com",
                "phone": "9876543210",
                "address": "New York",
                "credit_score": 780
            }
        }


class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    address: str | None = None
    credit_score: float | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str
    credit_score: float

    class Config:
        from_attributes = True