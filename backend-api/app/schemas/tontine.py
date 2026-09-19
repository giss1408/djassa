from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class TontineGroupCreate(BaseModel):
    name: str
    organizer_id: str
    contribution_amount: float
    currency: Optional[str] = "XOF"
    frequency: Optional[str] = "monthly"
    max_members: Optional[int] = None
    description: Optional[str] = None


class TontineGroupOut(BaseModel):
    id: int
    name: str
    organizer_id: str
    contribution_amount: float
    currency: str
    frequency: str
    max_members: Optional[int]
    description: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class JoinRequest(BaseModel):
    user_id: str


class ContributionCreate(BaseModel):
    user_id: str
    amount: float
    currency: Optional[str] = None
    payment_reference: Optional[str] = None


class CycleOut(BaseModel):
    id: int
    cycle_number: int
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    status: str

    class Config:
        orm_mode = True
