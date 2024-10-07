from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, get_db, recreate_db , Base
from routers.credit import router as credits_router
from routers.company import router as companies_router

app = FastAPI()

@app.on_event("startup")
async def startup():
    # await recreate_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(credits_router, prefix="/credits", tags=["credits"])
app.include_router(companies_router, prefix="/companies", tags=["companies"])