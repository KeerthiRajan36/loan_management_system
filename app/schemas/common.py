from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int