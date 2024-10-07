# API Endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.company import CompanyDB
from models.credit import CreditDB
from models.loan import LoanDB
from models.annual_turnover import AnnualTurnoverDB
from schemas.credit import Credit, CreditCreate
from schemas.loan import *
from schemas.annual_turnover import *
from database import get_db
import datetime

router = APIRouter()


@router.get("/", response_model=list[Credit])
async def get_all_credits(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CreditDB))
    all_credits = result.scalars().all()
    print(all_credits)
    return all_credits


@router.get("/{id}", response_model=Credit)
async def get_credit(id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(CreditDB).where(CreditDB.company_id == id))
        company_credit = result.scalar_one()

        if company_credit is None:
            raise HTTPException(status_code=404, detail="Credit not found")

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Credit not found")
    return company_credit


@router.post("/", response_model=Credit)
async def create_credit(credit_data: CreditCreate, company_id: int):
    # For simplicity, we will just return the received data as if it was stored
    total_due_loans = sum(
        loan.loan_amount for loan in credit_data.loans if loan.loan_status == "DUE"
    )
    total_turnover = sum(
        turnover.annual_turnover for turnover in credit_data.annual_turnover
    )

    credit_value = total_turnover - total_due_loans

    # Construct a simulated Credit response object
    simulated_credit = Credit(
        id=1,
        credit_value=credit_value,
        company_id=company_id,
        company_name=credit_data.company_name, 
        last_updated_at=datetime.datetime.utcnow(), 
    )

    return simulated_credit


@router.put("/{id}", response_model=Credit)
async def update_credit(
    id: int, credit_data: CreditCreate, db: AsyncSession = Depends(get_db)
):
    # Fetch the company for which we are updating credit
    result = await db.execute(select(CompanyDB).where(CompanyDB.id == id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Delete old records for loans and turnovers
    await db.execute(delete(LoanDB).where(LoanDB.company_id == company.id))
    await db.execute(
        delete(AnnualTurnoverDB).where(AnnualTurnoverDB.company_id == company.id)
    )

    # Insert new loans
    total_due_loans = 0
    for loan in credit_data.loans:
        new_loan = LoanDB(
            loan_amount=loan.loan_amount,
            taken_on=loan.taken_on,
            loan_bank_provider=loan.loan_bank_provider,
            loan_status=loan.loan_status,
            company_id=company.id,
        )
        db.add(new_loan)
        if loan.loan_status == "DUE":
            total_due_loans += loan.loan_amount

    # Insert new annual turnovers
    for turnover in credit_data.annual_turnover:
        new_turnover = AnnualTurnoverDB(
            annual_turnover=turnover.annual_turnover,
            profit=turnover.profit,
            fiscal_year=turnover.fiscal_year,
            reported_by_company_date=turnover.reported_by_company_date,
            company_id=company.id,
        )
        db.add(new_turnover)

    sorted_turnovers = sorted(
        credit_data.annual_turnover, key=lambda x: x.fiscal_year, reverse=True
    )

    total_turnover = 0
    for i, turnover in enumerate(sorted_turnovers):
        if i >= 2:
            break
        total_turnover += turnover.annual_turnover

    # Compute the updated credit value
    credit_value = total_turnover - total_due_loans

    # Update the credit information in CreditDB
    result = await db.execute(select(CreditDB).where(CreditDB.company_id == company.id))
    existing_credit = result.scalar_one_or_none()

    if existing_credit:
        existing_credit.credit_value = credit_value
        await db.commit()
        await db.refresh(existing_credit)
        return existing_credit
    else:
        new_credit = CreditDB(
            credit_value=credit_value,
            company_id=company.id,
            company_name=company.name,  # Assuming the company name is stored here
        )
        db.add(new_credit)
        await db.commit()
        await db.refresh(new_credit)
        return new_credit


@router.delete("/{id}")
async def delete_credit(id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(CompanyDB).where(CompanyDB.id == id))
    company = result.scalar_one_or_none()

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    await db.execute(delete(LoanDB).where(LoanDB.company_id == company.id))
    await db.execute(
        delete(AnnualTurnoverDB).where(AnnualTurnoverDB.company_id == company.id)
    )
    await db.execute(delete(CreditDB).where(CreditDB.company_id == company.id))

    await db.commit()
    print("Deleted {}", id)
    return {"detail": "Credit and related info deleted successfully"}
