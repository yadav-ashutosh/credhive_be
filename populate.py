from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from models import CompanyDB, LoanDB, AnnualTurnoverDB, CreditDB
from database import get_db, engine
import asyncio

# Create a Faker instance
fake = Faker()

# Generate fake company data
def generate_company_data():
    return {
        "name": fake.company(),
        "company_id": fake.unique.uuid4(),  # Use UUID as unique company ID
        "address": fake.address(),
        "registration_date": fake.date_between(start_date="-10y", end_date="today"),
        "num_employees": fake.random_int(min=10, max=5000),
        "contact_number": fake.phone_number(),
        "contact_email": fake.company_email(),
        "company_website": fake.domain_name(),
    }

# Generate fake loan data
def generate_loan_data():
    return {
        "loan_amount": fake.random_int(min=10000, max=5000000),
        "taken_on": fake.date_between(start_date="-5y", end_date="today"),
        "loan_bank_provider": fake.company(),
        "loan_status": fake.random_element(elements=("PAID", "DUE", "INITIATED")),
    }

# Generate fake annual turnover data
def generate_annual_turnover_data():
    return {
        "annual_turnover": fake.random_int(min=100000, max=10000000),
        "profit": fake.random_int(min=50000, max=5000000),
        "fiscal_year": f"{fake.year()}-{int(fake.year()) + 1}",
        "reported_by_company_date": fake.date_this_year(),
    }

# Populate the database with dummy data
async def populate_db(session: AsyncSession, num_companies: int = 10):
    for _ in range(num_companies):
        # Create fake company data
        company_data = generate_company_data()
        new_company = CompanyDB(**company_data)
        session.add(new_company)
        await session.commit()
        await session.refresh(new_company)

        # Create fake loans for the company
        for _ in range(3):  # Create 3 loans per company
            loan_data = generate_loan_data()
            new_loan = LoanDB(**loan_data, company_id=new_company.id)
            session.add(new_loan)

        # Create fake annual turnover for the company
        for _ in range(2):  # Create 2 annual turnovers per company
            turnover_data = generate_annual_turnover_data()
            new_turnover = AnnualTurnoverDB(**turnover_data, company_id=new_company.id)
            session.add(new_turnover)

    await session.commit()
    print(f"Successfully populated {num_companies} companies with loans and turnovers.")

# Main function to run the population
async def main():
    async with engine.begin() as conn:
        # Create a new session for database interaction
        async_session = sessionmaker(bind=conn, class_=AsyncSession)
        async with async_session() as session:
            await populate_db(session, num_companies=10)  # You can change the number of companies here

# If running the file directly, execute the population process
if __name__ == "__main__":
    asyncio.run(main())

