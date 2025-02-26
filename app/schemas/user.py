from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# UserCreate schema: used for registering a new user
class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)  # type: ignore
    email: EmailStr
    password: str
    referral_code: Optional[str] = None  # Optional since it's not required for all users

    class Config:
        orm_mode = True

# UserResponse schema: used for the response when fetching user details
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    referral_code: str
    referred_by: Optional[int] = None  # Can be None if the user wasn't referred
    created_at: str  # Use ISO 8601 formatted date string

    class Config:
        orm_mode = True

# Token schema: used for the authentication token response
class Token(BaseModel):
    access_token: str
    token_type: str

# TokenData schema: used to extract token-related data
class TokenData(BaseModel):
    username: str

    class Config:
        orm_mode = True

# PasswordResetRequest schema: used when requesting a password reset
class PasswordResetRequest(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

# PasswordResetConfirm schema: used when confirming the password reset with the token
class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

    class Config:
        orm_mode = True
