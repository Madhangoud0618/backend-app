from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    referral_code = Column(String(12), unique=True, index=True)
    referred_by = Column(Integer, ForeignKey('users.id'), index=True)
    created_at = Column(String(30), default=datetime.now(timezone.utc).isoformat())

    # Relationships
    referrals = relationship('Referral', back_populates='referrer', foreign_keys='Referral.referrer_id')

class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    referrer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    referred_user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    date_referred = Column(String(30), default=datetime.now(timezone.utc).isoformat())
    status = Column(String(20), default="pending")

    # Relationships
    referrer = relationship("User", back_populates="referrals", foreign_keys=[referrer_id])  # explicitly set the foreign key
    referred_user = relationship("User", foreign_keys=[referred_user_id])  # explicitly set the foreign key

# Create the index on referrer_id and status
Index('idx_referrer_status', Referral.referrer_id, Referral.status)
