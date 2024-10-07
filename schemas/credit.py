from pydantic import BaseModel, Field
from typing import List
from schemas.loan import *
from schemas.annual_turnover import *


class CreditCreate(BaseModel):
    loans: List[LoanCreate]
    annual_turnover: List[AnnualTurnoverCreate]

    class Config:
        orm_mode = True


class Credit(BaseModel):
    id: int
    credit_value: float
    company_id: int
    company_name: str = Field(..., min_length=1)

    class Config:
        orm_mode = True
