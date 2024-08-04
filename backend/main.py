# from fastapi import Depends, FastAPI, HTTPException, Request
# from pydantic import BaseModel
# from fastapi_users.exceptions import UserAlreadyExists
# from fastapi.security import OAuth2PasswordRequestForm
# from fastapi_users.router import ErrorCode
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_users import FastAPIUsers, schemas, BaseUserManager, IntegerIDMixin
# from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
# from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from contextlib import asynccontextmanager
from typing import Optional
import uvicorn
from app.app import app
import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Database setup
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"


# class Base(DeclarativeBase):
#     pass


# engine = create_async_engine(DATABASE_URL)
# async_session_maker = sessionmaker(
#     engine, class_=AsyncSession, expire_on_commit=False)

# # User model


# class User(SQLAlchemyBaseUserTable[int], Base):
#     id = Column(Integer, primary_key=True)
#     email = Column(String, nullable=False, unique=True)
#     hashed_password = Column(String, nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_superuser = Column(Boolean, default=False, nullable=False)
#     is_verified = Column(Boolean, default=False, nullable=False)
#     # role = Column(Integer, primary_key=False)


# class UserCreate(schemas.BaseUserCreate):
#     pass


# class UserUpdate(schemas.BaseUserUpdate):
#     pass


# class UserRead(schemas.BaseUser[int]):
#     id: int

#     class Config:
#         from_attributes = True


# class LoginResponse(BaseModel):
#     access_token: str
#     token_type: str
#     user: str
#     id: int
#     is_active: bool
#     role: bool

# # User database


# async def get_async_session():
#     async with async_session_maker() as session:
#         yield session


# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)

# # JWT authentication
# SECRET = "your-secret-key"
# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )

# # User Manager


# class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
#     reset_password_token_secret = SECRET
#     verification_token_secret = SECRET

#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         logger.info(f"User {user.id} has registered.")

#     async def create(self, user_create: UserCreate, safe: bool = False, request: Optional[Request] = None) -> User:
#         try:
#             return await super().create(user_create, request=request)
#         except UserAlreadyExists:
#             logger.error(f"User with email {user_create.email} already exists")
#             raise HTTPException(
#                 status_code=400,
#                 detail="REGISTER_USER_ALREADY_EXISTS",
#             )
#         except Exception as e:
#             logger.error(f"Failed to create user: {str(e)}")
#             raise


# async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
#     yield UserManager(user_db)

# # FastAPI Users instance
# fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

# # Lifespan event


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_db_and_tables()
#     yield

# # FastAPI app
# app = FastAPI(lifespan=lifespan)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.middleware("http")
# async def log_request(request: Request, call_next):
#     # Log the request details
#     logger.info(f"Received request: {request.method} {request.url}")
#     logger.info(f"Headers: {dict(request.headers)}")

#     # For POST requests, log the body
#     if request.method == "POST":
#         body = await request.body()
#         logger.info(f"Body: {body.decode()}")

#     response = await call_next(request)
#     return response


# @app.exception_handler(HTTPException)
# async def http_exception_handler(request: Request, exc: HTTPException):
#     logger.error(f"HTTP error occurred: {exc.detail}")
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"message": exc.detail},
#     )


# app.add_exception_handler(HTTPException, http_exception_handler)

# # Include FastAPI Users routes


# @app.post("/auth/jwt/login", response_model=LoginResponse)
# async def login(
#     request: Request,
#     credentials: OAuth2PasswordRequestForm = Depends(),
#     user_manager: UserManager = Depends(get_user_manager),
# ):
#     try:
#         user = await user_manager.authenticate(credentials)
#     except Exception as e:
#         logger.error(f"Login failed: {str(e)}")
#         raise HTTPException(
#             status_code=400,
#             detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#         )

#     if user is None or not user.is_active:
#         raise HTTPException(
#             status_code=400,
#             detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#         )

#     access_token = await auth_backend.get_strategy().write_token(user)
#     return LoginResponse(
#         access_token=access_token,
#         token_type="bearer",
#         user=user.email,
#         id=user.id,
#         is_active=user.is_active,
#         role=user.is_superuser
#     )
# # app.include_router(
# #     fastapi_users.get_auth_router(auth_backend),
# #     prefix="/auth/jwt",
# #     tags=["auth"]
# # )
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"]
# )

# # Root route


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
