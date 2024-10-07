from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base


class CompanyDB(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    company_id = Column(String, unique=True, index=True)
    address = Column(String)
    registration_date = Column(Date)
    num_employees = Column(Integer)
    contact_number = Column(String)
    contact_email = Column(String)
    company_website = Column(String)

    loans = relationship("LoanDB", back_populates="company")
    turnovers = relationship("AnnualTurnoverDB", back_populates="company")
    credits = relationship("CreditDB", back_populates="company")
