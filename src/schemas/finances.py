from datetime import datetime

from pydantic import BaseModel

class WriteSingleTransactionSchema(BaseModel):
    description: str
    is_income: bool = True
    value: float
    date: datetime | None

class ReadSingleTransactionSchema(WriteSingleTransactionSchema):
    id: int

