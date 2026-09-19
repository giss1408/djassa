from pydantic import BaseModel
from typing import Any, Dict


class WebhookIn(BaseModel):
    transaction_id: str | None
    id: str | None
    data: Dict[str, Any] | None

    class Config:
        extra = "allow"
