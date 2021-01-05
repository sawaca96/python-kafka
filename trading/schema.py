from uuid import UUID
from pydantic import BaseModel


class Account(BaseModel):
    start_cash: int
    name: str


class Order(BaseModel):
    account_id: UUID
    code: str
    price: int
    quantity: int
    side: str
