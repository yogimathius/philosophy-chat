"""Conversation model for managing philosophical dialogues."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Conversation(Base):
    """Conversation model for philosophical dialogues."""
    
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Conversation metadata
    title = Column(String(255), nullable=True)  # Auto-generated or user-set
    summary = Column(Text, nullable=True)  # AI-generated conversation summary
    philosophical_tradition = Column(String(100), nullable=True)  # Primary tradition
    conversation_type = Column(
        String(50), 
        default="general"
    )  # general, guided_inquiry, reflection, debate
    theme = Column(String(100), nullable=True)  # Conversation theme/topic
    
    # Context and memory
    context_data = Column(JSON, default=dict)  # Conversation context and memory
    key_concepts = Column(JSON, default=list)  # Extracted philosophical concepts
    emotional_journey = Column(JSON, default=list)  # Track emotional tone over time
    
    # Conversation status
    is_active = Column(Boolean, default=True)
    is_archived = Column(Boolean, default=False)
    
    # Quality metrics
    depth_score = Column(String(20), nullable=True)  # Overall philosophical depth
    engagement_level = Column(String(20), nullable=True)  # User engagement
    learning_progress = Column(JSON, default=dict)  # Track conceptual understanding
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship(
        "Message", 
        back_populates="conversation", 
        cascade="all, delete-orphan",
        order_by="Message.created_at"
    )
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, title={self.title})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert conversation to dictionary representation."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "title": self.title,
            "summary": self.summary,
            "philosophical_tradition": self.philosophical_tradition,
            "conversation_type": self.conversation_type,
            "theme": self.theme,
            "context_data": self.context_data or {},
            "key_concepts": self.key_concepts or [],
            "emotional_journey": self.emotional_journey or [],
            "is_active": self.is_active,
            "is_archived": self.is_archived,
            "depth_score": self.depth_score,
            "engagement_level": self.engagement_level,
            "learning_progress": self.learning_progress or {},
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity": self.last_activity.isoformat(),
        }
    
    def update_activity(self) -> None:
        """Update the last activity timestamp."""
        self.last_activity = datetime.utcnow()
    
    def add_concept(self, concept: str) -> None:
        """Add a philosophical concept to the conversation."""
        concepts = self.key_concepts or []
        if concept not in concepts:
            concepts.append(concept)
            self.key_concepts = concepts
    
    def add_emotional_point(self, emotion: str, timestamp: Optional[datetime] = None) -> None:
        """Add an emotional data point to the journey."""
        journey = self.emotional_journey or []
        journey.append({
            "emotion": emotion,
            "timestamp": (timestamp or datetime.utcnow()).isoformat()
        })
        self.emotional_journey = journey
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update conversation context data."""
        context = self.context_data or {}
        context.update(new_context)
        self.context_data = context
    
    def get_recent_messages(self, limit: int = 10) -> List["Message"]:
        """Get the most recent messages from this conversation."""
        return sorted(self.messages, key=lambda m: m.created_at, reverse=True)[:limit]
    
    def generate_title(self, ai_service) -> str:
        """Generate a title for the conversation based on content."""
        if not self.messages or len(self.messages) < 2:
            return f"Conversation on {self.created_at.strftime('%B %d, %Y')}"
        
        # This would be implemented with the AI service
        # For now, return a simple title based on tradition and theme
        parts = []
        if self.philosophical_tradition:
            parts.append(self.philosophical_tradition.title())
        if self.theme:
            parts.append(f"on {self.theme}")
        
        if parts:
            return " ".join(parts)
        return f"Philosophical Discussion - {self.created_at.strftime('%B %d')}"