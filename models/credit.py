from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from database import Base


class CreditDB(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    credit_value = Column(Float)
    company_id = Column(Integer, ForeignKey("companies.id"))
    company_name = Column(String, index=True)
    last_updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    company = relationship("CompanyDB", back_populates="credits")

    def __init__(self, credit_value, company_id, company_name):
        self.credit_value = credit_value
        self.company_id = company_id
        self.company_name = company_name
