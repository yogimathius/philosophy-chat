"""Authentication-related Pydantic schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr = Field(..., description="User email address")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=8, max_length=100, description="User password")
    full_name: Optional[str] = Field(None, max_length=200, description="Full name")
    
    @validator("username")
    def validate_username(cls, v):
        if v and not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Username can only contain letters, numbers, hyphens, and underscores")
        return v
    
    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, and one digit")
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "email": "philosopher@example.com",
                "username": "wisdom_seeker",
                "password": "SecurePass123",
                "full_name": "Alex Philosopher"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "philosopher@example.com",
                "password": "SecurePass123"
            }
        }


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user_id: str = Field(..., description="User ID")
    
    class Config:
        schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class TokenData(BaseModel):
    """Schema for token data."""
    user_id: Optional[str] = None
    email: Optional[str] = None


class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr = Field(..., description="Email address for password reset")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "philosopher@example.com"
            }
        }


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, and one digit")
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "token": "reset-token-12345",
                "new_password": "NewSecurePass123"
            }
        }


class ChangePassword(BaseModel):
    """Schema for password change."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @validator("new_password")
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        
        if not (has_upper and has_lower and has_digit):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, and one digit")
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "current_password": "OldSecurePass123",
                "new_password": "NewSecurePass123"
            }
        }