from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.auth.schemas import UserCreate, UserLogin, Token, UserResponse
from app.auth.utils import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.models.user import User, Session
from app.settings import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserCreate):
    # Check if user exists
    if await User.exists(email=user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    if await User.exists(username=user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )

    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = await User.create(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )

    return user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # Create session
    expires_at = datetime.utcnow() + access_token_expires
    await Session.create(user=user, token=access_token, expires_at=expires_at)

    return Token(access_token=access_token)


@router.post("/logout")
async def logout(credentials: HTTPBearer = Depends(security)):
    # Deactivate the current session
    await Session.filter(token=credentials.credentials, is_active=True).update(
        is_active=False
    )
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user
