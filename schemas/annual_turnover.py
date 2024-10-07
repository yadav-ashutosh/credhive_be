from pydantic import BaseModel, Field, field_validator
import datetime


class AnnualTurnoverCreate(BaseModel):
    annual_turnover: float = Field(..., ge=0)
    profit: float = Field(..., ge=0)
    fiscal_year: str
    reported_by_company_date: datetime.date

    @field_validator("fiscal_year")
    def validate_fiscal_year(cls, value):
        if not value.isdigit() or len(value) != 4:
            raise ValueError("Fiscal year must be a 4-digit number (e.g., 2023)")
        return value

    class Config:
        orm_mode = True
