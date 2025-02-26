from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.utils.security import get_current_user
from ..models.user import User
from ..models.user import Referral
from ..schemas.referral import ReferralStats

router = APIRouter(tags=["Referrals"])

@router.get("/referrals")
async def get_user_referrals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Referral)
        .filter(Referral.referrer_id == current_user.id)
        .order_by(Referral.date_referred.desc())
    )
    referrals = result.scalars().all()
    return referrals

@router.get("/referral-stats", response_model=ReferralStats)
async def get_referral_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(func.count(Referral.id))
        .filter(Referral.referrer_id == current_user.id)
        .filter(Referral.status == "successful")
    )
    total_referrals = result.scalar()
    
    return {
        "total_referrals": total_referrals,
        "active_referrals": total_referrals,  # Modify based on your business logic
        "pending_referrals": 0
    }