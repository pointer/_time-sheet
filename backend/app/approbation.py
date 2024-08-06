from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_async_session, Approbation, TimeSheet
from app.schemas import ApprobationCreate, ApprobationUpdate, ApprobationRead
from app.users import current_active_user, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/approbation", response_model=ApprobationRead)
async def create_approbation(approbation: ApprobationCreate, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    db_approbation = Approbation(
        **approbation.model_dump(), supervisor_id=user.id)
    db.add(db_approbation)
    await db.commit()
    await db.refresh(db_approbation)

    # Update the timesheet status
    timesheet = await db.query(TimeSheet).filter(TimeSheet.id == approbation.timesheet_id).first()
    if timesheet:
        timesheet.status = 'approved' if approbation.approved else 'rejected'
        await db.commit()

    return db_approbation


@router.get("/approbations/", response_model=List[ApprobationRead])
async def read_approbations(skip: int = 0, limit: int = 100, user: User = Depends(current_active_user), db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Approbation).offset(skip).limit(limit))
    approbations = result.scalars().all()
    return approbations


@router.get("/approbations/{approbation_id}", response_model=ApprobationRead)
async def read_approbation(approbation_id: int, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    approbation = await db.query(Approbation).filter(Approbation.id == approbation_id).first()
    if approbation is None:
        raise HTTPException(status_code=404, detail="Approbation not found")
    return approbation


@router.put("/approbation/{approbation_id}", response_model=ApprobationRead)
async def update_approbation(approbation_id: int, approbation: ApprobationUpdate, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    db_approbation = await db.query(Approbation).filter(Approbation.id == approbation_id).first()
    if db_approbation is None:
        raise HTTPException(status_code=404, detail="Approbation not found")

    for key, value in approbation.model_dump().items():
        setattr(db_approbation, key, value)

    await db.commit()
    await db.refresh(db_approbation)

    # Update the timesheet status
    timesheet = await db.query(TimeSheet).filter(TimeSheet.id == db_approbation.timesheet_id).first()
    if timesheet:
        timesheet.status = 'approved' if db_approbation.approved else 'rejected'
        await db.commit()

    return db_approbation
