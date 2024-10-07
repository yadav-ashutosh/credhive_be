from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class AnnualTurnoverDB(Base):
    __tablename__ = "annual_turnovers"

    id = Column(Integer, primary_key=True, index=True)
    annual_turnover = Column(Float)
    profit = Column(Float)
    fiscal_year = Column(String)
    reported_by_company_date = Column(Date)
    company_id = Column(Integer, ForeignKey("companies.id"))

    company = relationship("CompanyDB", back_populates="turnovers")
