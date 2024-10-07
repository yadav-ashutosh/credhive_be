from pydantic import BaseModel, Field, field_validator
import datetime


class LoanCreate(BaseModel):
    loan_amount: float = Field(..., gt=0)
    taken_on: datetime.date
    loan_bank_provider: str
    loan_status: str  # PAID, DUE, INITIATED

    @field_validator("loan_status")
    def check_loan_status(cls, value):
        allowed_status = {"PAID", "DUE", "INITIATED"}
        if value not in allowed_status:
            raise ValueError(f"Loan status must be one of {allowed_status}")
        return value

    class Config:
        orm_mode = True
