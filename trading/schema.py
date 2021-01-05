from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Account(BaseModel):
    start_cash: int
    name: str


class Order(BaseModel):
    account_id: UUID
    code: str
    price: int
    quantity: int
    side: str
