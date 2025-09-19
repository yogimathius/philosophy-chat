"""User model for authentication and preferences."""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for philosophical AI companion users."""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Philosophical preferences
    philosophical_preferences = Column(JSON, default=dict)  # traditions, complexity, interests
    learning_level = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    preferred_learning_style = Column(
        String(50), 
        default="socratic"
    )  # socratic, explanatory, contemplative
    
    # Daily wisdom settings
    daily_wisdom_enabled = Column(Boolean, default=True)
    wisdom_delivery_time = Column(String(10), default="09:00")  # HH:MM format
    timezone = Column(String(50), default="UTC")
    
    # User status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_active = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    reflections = relationship("UserReflection", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary representation."""
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "bio": self.bio,
            "philosophical_preferences": self.philosophical_preferences or {},
            "learning_level": self.learning_level,
            "preferred_learning_style": self.preferred_learning_style,
            "daily_wisdom_enabled": self.daily_wisdom_enabled,
            "wisdom_delivery_time": self.wisdom_delivery_time,
            "timezone": self.timezone,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    @property
    def preferred_traditions(self) -> list[str]:
        """Get user's preferred philosophical traditions."""
        prefs = self.philosophical_preferences or {}
        return prefs.get("traditions", ["stoicism", "existentialism", "buddhism"])
    
    @property
    def philosophical_interests(self) -> list[str]:
        """Get user's philosophical interests."""
        prefs = self.philosophical_preferences or {}
        return prefs.get("interests", ["ethics", "meaning", "consciousness"])
    
    def update_last_active(self) -> None:
        """Update the user's last active timestamp."""
        self.last_active = datetime.utcnow()
    
    def update_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user's philosophical preferences."""
        current_prefs = self.philosophical_preferences or {}
        current_prefs.update(preferences)
        self.philosophical_preferences = current_prefs