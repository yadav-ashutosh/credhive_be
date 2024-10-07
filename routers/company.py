# API Endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.company import CompanyDB
from schemas.company import *
from database import get_db
import datetime

router = APIRouter()


def update_company_(
    existing_company: CompanyDB, company_data: BaseModel, db: AsyncSession
):
    """
    Common function to update the company entry with new data.
    This will update only the fields that are provided (non-None values).
    """
    for var, value in vars(company_data).items():
        if value is not None:
            setattr(existing_company, var, value)


@router.post("/company", response_model=Company)
async def add_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    # Check if company exists
    result = await db.execute(
        select(CompanyDB).where(CompanyDB.company_id == company.company_id)
    )
    existing_company = result.scalar_one_or_none()

    if existing_company:
        update_company_(existing_company, company, db)
        await db.commit()
        await db.refresh(existing_company)
        return existing_company

    # If company does not exist, add a new entry
    new_company = CompanyDB(**company.dict(exclude={"annual_turnover", "loans"}))
    db.add(new_company)
    await db.commit()
    await db.refresh(new_company)
    return new_company


@router.put("/company", response_model=Company)
async def update_company(company: CompanyUpdate, db: AsyncSession = Depends(get_db)):
    # Check if company exists by ID
    result = await db.execute(
        select(CompanyDB).where(CompanyDB.company_id == company.company_id)
    )
    existing_company = result.scalar_one_or_none()

    if not existing_company:
        raise HTTPException(status_code=404, detail="Company not found")

    # Use the common update function to update the company
    update_company_(existing_company, company, db)

    await db.commit()
    await db.refresh(existing_company)
    return existing_company
