from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi_users.exceptions import UserAlreadyExists
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.router import ErrorCode
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users import FastAPIUsers, password, schemas, BaseUserManager, IntegerIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
# from fastapi_users.db import SQLAlchemyUserDatabase

from pydantic import BaseModel
from app.db import User, create_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
import logging
from app.users import UserManager, get_user_manager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: str
    id: int
    is_active: bool
    role: bool


class RegisterResponse(BaseModel):
    pass


@app.middleware("http")
async def log_request(request: Request, call_next):
    # Log the request details
    logger.info(f"Received request: {request.method} {request.url}")
    logger.info(f"Headers: {dict(request.headers)}")

    # For POST requests, log the body
    if request.method == "POST":
        body = await request.body()
        logger.info(f"Body: {body.decode()}")

    response = await call_next(request)
    return response


@app.post("/auth/register", response_model=UserRead)
async def register(
    user: UserCreate,
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        created_user = await user_manager.create(user)
        logger.info(f"User {created_user.id} has registered.")
        return UserRead(
            id=created_user.id,
            email=created_user.email,
            is_active=created_user.is_active,
            is_superuser=created_user.is_superuser,
            is_verified=created_user.is_verified,
            password=created_user.password,
            passconfirm=created_user.passconfirm,
            phone=created_user.phone,
            role=created_user.role,
            contractNumber=created_user.contractNumber,
            company=created_user.company,
            taxNumber=created_user.taxNumber,
            client=created_user.client,
            project=created_user.project,
            city=created_user.city,
            zip=created_user.zip,
            dateStart=created_user.dateStart,
            dateEnd=created_user.dateEnd,
            rate=created_user.rate,
        )
    except UserAlreadyExists:
        logger.error(f"Registration failed: User with email {
                     user.email} already exists")
        raise HTTPException(
            status_code=400,
            detail="REGISTER_USER_ALREADY_EXISTS",
        )
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred during registration",
        )


@app.post("/auth/jwt/login", response_model=LoginResponse)
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        user = await user_manager.authenticate(credentials)
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=400,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )

    access_token = await auth_backend.get_strategy().write_token(user)
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user.email,
        id=user.id,
        is_active=user.is_active,
        role=user.is_superuser
    )

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
