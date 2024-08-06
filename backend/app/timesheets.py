from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_async_session, TimeSheet
from app.schemas import TimeSheetCreate, TimeSheetUpdate, TimeSheetRead
from app.users import current_active_user, User

router = APIRouter()


@router.post("/timesheet", response_model=TimeSheetRead)
async def create_timesheet(timesheet: TimeSheetCreate, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    db_timesheet = TimeSheet(**timesheet.model_dump(), user_id=user.id)
    db.add(db_timesheet)
    await db.commit()
    await db.refresh(db_timesheet)
    return db_timesheet


# @router.post("/timesheet", response_model=TimeSheetRead)
# async def create_timesheet(timesheet: TimeSheetCreate, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
#     db_timesheet = TimeSheet(**timesheet.dict(), user_id=user.id)
#     db.add(db_timesheet)
#     db.commit()
#     db.refresh(db_timesheet)
#     return db_timesheet


@router.get("/timesheets/", response_model=List[TimeSheetRead])
async def read_timesheets(skip: int = 0, limit: int = 100, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    timesheets = db.query(TimeSheet).filter(
        TimeSheet.user_id == user.id).offset(skip).limit(limit).all()
    return timesheets


@router.get("/timesheets/{month}", response_model=List[TimeSheetRead])
async def read_timesheets_by_month(month: str, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    timesheets = db.query(TimeSheet).filter(
        TimeSheet.user_id == user.id, TimeSheet.month == month).all()
    return timesheets


@router.put("/timesheet/{timesheet_id}", response_model=TimeSheetRead)
async def update_timesheet(timesheet_id: int, timesheet: TimeSheetUpdate, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    db_timesheet = db.query(TimeSheet).filter(
        TimeSheet.id == timesheet_id, TimeSheet.user_id == user.id).first()
    if db_timesheet is None:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    for key, value in timesheet.dict(exclude_unset=True).items():
        setattr(db_timesheet, key, value)
    db.commit()
    db.refresh(db_timesheet)
    return db_timesheet


@router.delete("/timesheet/{timesheet_id}", response_model=TimeSheetRead)
async def delete_timesheet(timesheet_id: int, user: User = Depends(current_active_user), db: Session = Depends(get_async_session)):
    db_timesheet = db.query(TimeSheet).filter(
        TimeSheet.id == timesheet_id, TimeSheet.user_id == user.id).first()
    if db_timesheet is None:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    db.delete(db_timesheet)
    db.commit()
    return db_timesheet
