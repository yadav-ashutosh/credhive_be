from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import datetime


class CompanyBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    company_id: str = Field(
        ..., min_length=1, max_length=30
    )  # Mandatory in both create and update
    address: Optional[str] = Field(None, min_length=1, max_length=300)
    registration_date: Optional[datetime.date] = None
    num_employees: Optional[int] = Field(None, ge=0)
    contact_number: Optional[str] = Field(None, min_length=5, max_length=17)
    contact_email: Optional[EmailStr] = None
    company_website: Optional[str] = Field(None, pattern=r"https?://\S+\.\S+")

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    name: str = Field(..., min_length=1, max_length=200)
    company_id: str = Field(..., min_length=1, max_length=30)
    address: Optional[str] = Field(None, min_length=1, max_length=300)
    registration_date: Optional[datetime.date] = None
    num_employees: Optional[int] = Field(None, ge=0)
    contact_number: Optional[str] = Field(None, min_length=5, max_length=17)
    contact_email: Optional[EmailStr] = None
    company_website: Optional[str] = Field(None, pattern=r"https?://\S+\.\S+")


class CompanyUpdate(CompanyBase):
    company_id: str = Field(..., min_length=1, max_length=30)
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    address: Optional[str] = Field(None, min_length=1, max_length=300)
    registration_date: Optional[datetime.date] = None
    num_employees: Optional[int] = Field(None, ge=0)
    contact_number: Optional[str] = Field(None, min_length=5, max_length=17)
    contact_email: Optional[EmailStr] = None
    company_website: Optional[str] = Field(None, pattern=r"https?://\S+\.\S+")


class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True
