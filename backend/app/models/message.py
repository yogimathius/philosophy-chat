"""Message model for individual conversation messages."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class Message(Base):
    """Message model for individual conversation messages."""
    
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    conversation_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("conversations.id"), 
        nullable=False, 
        index=True
    )
    
    # Message content
    sender = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    
    # NLP Analysis Results
    philosophical_concepts = Column(JSON, default=list)  # Extracted concepts
    emotional_tone = Column(String(50), nullable=True)  # Detected emotion
    complexity_score = Column(Integer, nullable=True)  # 1-10 complexity rating
    depth_indicators = Column(JSON, default=list)  # Philosophical depth markers
    
    # AI Response Metadata (for assistant messages)
    ai_model_used = Column(String(100), nullable=True)  # GPT-4, Claude, etc.
    philosophical_tradition_used = Column(String(100), nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    token_count = Column(Integer, nullable=True)
    
    # User Interaction (for user messages)
    edit_history = Column(JSON, default=list)  # Track message edits
    user_feedback = Column(String(20), nullable=True)  # thumbs up/down/etc.
    
    # Quality Assessment
    coherence_score = Column(Integer, nullable=True)  # 1-10 coherence rating
    relevance_score = Column(Integer, nullable=True)  # 1-10 relevance to conversation
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self) -> str:
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, sender={self.sender}, content='{preview}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary representation."""
        return {
            "id": str(self.id),
            "conversation_id": str(self.conversation_id),
            "sender": self.sender,
            "content": self.content,
            "philosophical_concepts": self.philosophical_concepts or [],
            "emotional_tone": self.emotional_tone,
            "complexity_score": self.complexity_score,
            "depth_indicators": self.depth_indicators or [],
            "ai_model_used": self.ai_model_used,
            "philosophical_tradition_used": self.philosophical_tradition_used,
            "response_time_ms": self.response_time_ms,
            "token_count": self.token_count,
            "edit_history": self.edit_history or [],
            "user_feedback": self.user_feedback,
            "coherence_score": self.coherence_score,
            "relevance_score": self.relevance_score,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def add_concept(self, concept: str, confidence: Optional[float] = None) -> None:
        """Add a philosophical concept to the message."""
        concepts = self.philosophical_concepts or []
        
        concept_entry = {"name": concept}
        if confidence is not None:
            concept_entry["confidence"] = confidence
            
        concepts.append(concept_entry)
        self.philosophical_concepts = concepts
    
    def set_analysis_results(
        self,
        concepts: List[str],
        emotional_tone: Optional[str] = None,
        complexity_score: Optional[int] = None,
        depth_indicators: Optional[List[str]] = None
    ) -> None:
        """Set NLP analysis results for the message."""
        self.philosophical_concepts = [{"name": concept} for concept in concepts]
        self.emotional_tone = emotional_tone
        self.complexity_score = complexity_score
        self.depth_indicators = depth_indicators or []
    
    def set_ai_metadata(
        self,
        model_used: str,
        response_time_ms: int,
        tradition_used: Optional[str] = None,
        token_count: Optional[int] = None
    ) -> None:
        """Set AI response metadata."""
        self.ai_model_used = model_used
        self.response_time_ms = response_time_ms
        self.philosophical_tradition_used = tradition_used
        self.token_count = token_count
    
    def add_edit(self, original_content: str, reason: Optional[str] = None) -> None:
        """Track message edits."""
        edits = self.edit_history or []
        edit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "original_content": original_content,
            "reason": reason
        }
        edits.append(edit_entry)
        self.edit_history = edits
    
    def set_feedback(self, feedback: str) -> None:
        """Set user feedback for the message."""
        valid_feedback = ["thumbs_up", "thumbs_down", "helpful", "unclear", "inspiring"]
        if feedback in valid_feedback:
            self.user_feedback = feedback
    
    @property
    def is_from_user(self) -> bool:
        """Check if message is from user."""
        return self.sender == "user"
    
    @property
    def is_from_assistant(self) -> bool:
        """Check if message is from assistant."""
        return self.sender == "assistant"
    
    @property
    def word_count(self) -> int:
        """Get word count of the message content."""
        return len(self.content.split())
    
    @property
    def concept_names(self) -> List[str]:
        """Get list of concept names from philosophical_concepts."""
        concepts = self.philosophical_concepts or []
        return [c.get("name", "") for c in concepts if isinstance(c, dict) and "name" in c]