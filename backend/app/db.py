from typing import AsyncGenerator
from datetime import datetime
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


class Base(DeclarativeBase):
    pass


# class User(SQLAlchemyBaseUserTableUUID, Base):
#     pass

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    role = Column(String, nullable=True)
    contract_number = Column(String, nullable=True)
    company = Column(String, nullable=True)
    company_id = Column(String, nullable=True)
    tax_number = Column(String, nullable=True)
    client = Column(String, nullable=True)
    project = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    date_start = Column(Date, nullable=True)
    date_end = Column(Date, nullable=True)
    rate = Column(Numeric, nullable=True)


class TimeSheet(Base):
    __tablename__ = "timesheet"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_account.id"))
    date = Column(Date, nullable=False)
    worked_days = Column(Integer, nullable=False)
    working_days = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    status = Column(String, default='pending')

    user = relationship("User", back_populates="timesheets")


User.timesheets = relationship("TimeSheet", back_populates="user")

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Approbation(Base):
    __tablename__ = "approbation"

    id = Column(Integer, primary_key=True, index=True)
    timesheet_id = Column(Integer, ForeignKey("timesheet.id"))
    supervisor_id = Column(Integer, ForeignKey("user_account.id"))
    approved = Column(Boolean, nullable=False)
    approval_date = Column(DateTime, default=datetime.utcnow)

    timesheet = relationship("TimeSheet", back_populates="approbations")
    supervisor = relationship("User", back_populates="approbations")


TimeSheet.approbations = relationship(
    "Approbation", back_populates="timesheet")

User.approbations = relationship("Approbation", back_populates="supervisor")


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
