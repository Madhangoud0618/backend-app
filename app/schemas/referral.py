from pydantic import BaseModel

# Schema for Referral Statistics
class ReferralStats(BaseModel):
    total_referrals: int
    active_referrals: int
    pending_referrals: int

    class Config:
        orm_mode = True
