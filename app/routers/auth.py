from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import Referral
from app.utils.helpers import generate_unique_referral_code
from ..schemas.user import UserCreate, UserResponse, Token
from ..models.user import User
from ..core.config import settings
from ..utils.security import get_password_hash, create_access_token, verify_password

router = APIRouter(tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check existing user
    existing_user = await db.execute(
        select(User).filter(
            (User.email == user_data.email) | 
            (User.username == user_data.username)
        )
    )
    if existing_user.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Generate referral code
    referral_code = generate_unique_referral_code()
    
    # Handle referral system
    referred_by = None
    if user_data.referral_code:
        referrer = await db.execute(
            select(User).filter(User.referral_code == user_data.referral_code)
        )
        referrer = referrer.scalars().first()
        if not referrer:
            raise HTTPException(status_code=400, detail="Invalid referral code")
        referred_by = referrer.id
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        referral_code=referral_code,
        referred_by=referred_by
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create referral record if applicable
    if referred_by:
        referral = Referral(
            referrer_id=referred_by,
            referred_user_id=user.id,
            status="successful"
        )
        db.add(referral)
        await db.commit()
    
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(
        select(User).filter(User.username == form_data.username)
    )
    user = user.scalars().first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}