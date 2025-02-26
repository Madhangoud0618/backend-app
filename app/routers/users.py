# app/routers/users.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.utils.security import create_access_token, get_password_hash
from ..schemas.user import PasswordResetRequest, PasswordResetConfirm
from ..core.config import settings

router = APIRouter(tags=["Users"])

@router.post("/forgot-password")
async def forgot_password(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    user = await db.execute(
        select(User).filter(User.email == request.email)
    )
    user = user.scalars().first()
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    
    # Generate password reset token (expires in 1 hour)
    reset_token = create_access_token(
        data={"sub": user.email},
        secret_key=settings.SECRET_KEY,
        expires_delta=timedelta(hours=1)
    )
    
    # In production: Send email with reset link
    print(f"Password reset token for {user.email}: {reset_token}")
    
    return {"message": "Password reset instructions sent"}

@router.post("/reset-password")
async def reset_password(
    request: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(
            request.token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = await db.execute(
        select(User).filter(User.email == email)
    )
    user = user.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update password
    user.password_hash = get_password_hash(request.new_password)
    await db.commit()
    
    return {"message": "Password updated successfully"}