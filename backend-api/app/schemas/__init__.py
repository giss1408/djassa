from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class Payment(BaseModel):
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(min_length=3, max_length=8)
    recipient_id: str = Field(min_length=1, max_length=128)


class PaymentOut(Payment):
    id: int


class Transaction(BaseModel):
    merchant_id: int
    user_id: str | None = None
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(min_length=3, max_length=8)
    type: str = Field(min_length=1, max_length=32)


class TransactionOut(Transaction):
    id: int
    timestamp: datetime


class Merchant(BaseModel):
    id: int | None = None
    name: str
    external_id: str | None = None
    description: str | None = None


class ConsentIn(BaseModel):
    user_id: str | None = None
    merchant_id: int
    scope: str = Field(min_length=1, max_length=255)


class ConsentOut(ConsentIn):
    id: int
    granted_at: datetime
