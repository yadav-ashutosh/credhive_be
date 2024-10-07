import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy Base for ORM models
Base = declarative_base()

# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure that DATABASE_URL is provided
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Create the async engine for connecting to the PostgreSQL database
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a sessionmaker bound to the async engine
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# Function to drop all tables and recreate them
async def recreate_db():
    """Drop all tables and recreate them."""
    # Import models here to ensure they are registered before metadata is created
    from models import (
        CompanyDB,
        LoanDB,
        CreditDB,
        AnnualTurnoverDB,
    )  # Import all your models

    async with engine.begin() as conn:
        # Drop all tables
        print("Dropping all tables...")
        await conn.run_sync(Base.metadata.drop_all)

        # Recreate all tables
        print("Creating all tables...")
        await conn.run_sync(Base.metadata.create_all)


# Dependency to get database session in FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
