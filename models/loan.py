from sqlalchemy import Column, Integer, Float, Date, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum


class LoanStatus(PyEnum):
    PAID = "PAID"
    DUE = "DUE"
    INITIATED = "INITIATED"


class LoanDB(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    loan_amount = Column(Float)
    taken_on = Column(Date)
    loan_bank_provider = Column(String)
    loan_status = Column(Enum(LoanStatus), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("CompanyDB", back_populates="loans")
