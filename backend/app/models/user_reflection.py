"""User reflection model for philosophical reflections and insights."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserReflection(Base):
    """User reflection model for philosophical reflections and insights."""
    
    __tablename__ = "user_reflections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    daily_wisdom_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("daily_wisdom.id"), 
        nullable=True, 
        index=True
    )
    
    # Reflection content
    reflection_text = Column(Text, nullable=False)
    reflection_type = Column(String(50), default="daily")  # daily, spontaneous, guided
    
    # NLP Analysis Results
    philosophical_depth_score = Column(Integer, nullable=True)  # 1-10 depth rating
    complexity_score = Column(Integer, nullable=True)  # 1-10 complexity rating
    emotional_tone = Column(String(50), nullable=True)  # Detected emotional state
    key_insights = Column(JSON, default=list)  # Extracted insights
    concepts_explored = Column(JSON, default=list)  # Philosophical concepts mentioned
    
    # Growth tracking
    growth_indicators = Column(JSON, default=list)  # Signs of philosophical development
    personal_connections = Column(JSON, default=list)  # Personal life connections
    questions_raised = Column(JSON, default=list)  # New questions emerged
    
    # Quality metrics
    coherence_score = Column(Integer, nullable=True)  # 1-10 coherence rating
    authenticity_score = Column(Integer, nullable=True)  # 1-10 authenticity rating
    practical_application_score = Column(Integer, nullable=True)  # 1-10 practical relevance
    
    # User self-assessment
    user_satisfaction_rating = Column(Integer, nullable=True)  # 1-5 user rating
    user_difficulty_rating = Column(Integer, nullable=True)  # 1-5 difficulty experienced
    time_spent_minutes = Column(Integer, nullable=True)  # Time spent reflecting
    
    # Follow-up and connections
    related_conversations = Column(JSON, default=list)  # Connected conversation IDs
    follow_up_actions = Column(JSON, default=list)  # Actions user plans to take
    book_recommendations = Column(JSON, default=list)  # Generated reading suggestions
    
    # Metadata
    reflection_context = Column(JSON, default=dict)  # Context when reflection was made
    is_private = Column(Boolean, default=True)
    is_favorite = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="reflections")
    daily_wisdom = relationship("DailyWisdom", back_populates="reflections")
    
    def __repr__(self) -> str:
        preview = self.reflection_text[:50] + "..." if len(self.reflection_text) > 50 else self.reflection_text
        return f"<UserReflection(id={self.id}, user_id={self.user_id}, content='{preview}')>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert reflection to dictionary representation."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "daily_wisdom_id": str(self.daily_wisdom_id) if self.daily_wisdom_id else None,
            "reflection_text": self.reflection_text,
            "reflection_type": self.reflection_type,
            "philosophical_depth_score": self.philosophical_depth_score,
            "complexity_score": self.complexity_score,
            "emotional_tone": self.emotional_tone,
            "key_insights": self.key_insights or [],
            "concepts_explored": self.concepts_explored or [],
            "growth_indicators": self.growth_indicators or [],
            "personal_connections": self.personal_connections or [],
            "questions_raised": self.questions_raised or [],
            "coherence_score": self.coherence_score,
            "authenticity_score": self.authenticity_score,
            "practical_application_score": self.practical_application_score,
            "user_satisfaction_rating": self.user_satisfaction_rating,
            "user_difficulty_rating": self.user_difficulty_rating,
            "time_spent_minutes": self.time_spent_minutes,
            "related_conversations": self.related_conversations or [],
            "follow_up_actions": self.follow_up_actions or [],
            "book_recommendations": self.book_recommendations or [],
            "reflection_context": self.reflection_context or {},
            "is_private": self.is_private,
            "is_favorite": self.is_favorite,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def add_insight(self, insight: str, confidence: Optional[float] = None) -> None:
        """Add a key insight from the reflection."""
        insights = self.key_insights or []
        insight_entry = {"text": insight, "timestamp": datetime.utcnow().isoformat()}
        if confidence:
            insight_entry["confidence"] = confidence
        insights.append(insight_entry)
        self.key_insights = insights
    
    def add_concept(self, concept: str, relevance: Optional[str] = None) -> None:
        """Add a philosophical concept explored in the reflection."""
        concepts = self.concepts_explored or []
        concept_entry = {"name": concept}
        if relevance:
            concept_entry["relevance"] = relevance
        concepts.append(concept_entry)
        self.concepts_explored = concepts
    
    def add_growth_indicator(self, indicator: str, category: Optional[str] = None) -> None:
        """Add a growth indicator identified in the reflection."""
        indicators = self.growth_indicators or []
        indicator_entry = {"description": indicator}
        if category:
            indicator_entry["category"] = category
        indicators.append(indicator_entry)
        self.growth_indicators = indicators
    
    def add_personal_connection(self, connection: str) -> None:
        """Add a personal life connection made in the reflection."""
        connections = self.personal_connections or []
        connections.append({
            "description": connection,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.personal_connections = connections
    
    def add_question(self, question: str) -> None:
        """Add a new question raised during reflection."""
        questions = self.questions_raised or []
        questions.append({
            "question": question,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.questions_raised = questions
    
    def add_follow_up_action(self, action: str, priority: Optional[str] = None) -> None:
        """Add a follow-up action the user plans to take."""
        actions = self.follow_up_actions or []
        action_entry = {"action": action, "added_at": datetime.utcnow().isoformat()}
        if priority:
            action_entry["priority"] = priority
        actions.append(action_entry)
        self.follow_up_actions = actions
    
    def add_book_recommendation(self, title: str, author: str, reason: str) -> None:
        """Add a book recommendation based on the reflection."""
        books = self.book_recommendations or []
        books.append({
            "title": title,
            "author": author,
            "reason": reason,
            "generated_at": datetime.utcnow().isoformat()
        })
        self.book_recommendations = books
    
    def set_analysis_scores(
        self,
        depth_score: Optional[int] = None,
        complexity_score: Optional[int] = None,
        coherence_score: Optional[int] = None,
        authenticity_score: Optional[int] = None,
        practical_score: Optional[int] = None
    ) -> None:
        """Set all analysis scores at once."""
        if depth_score is not None:
            self.philosophical_depth_score = depth_score
        if complexity_score is not None:
            self.complexity_score = complexity_score
        if coherence_score is not None:
            self.coherence_score = coherence_score
        if authenticity_score is not None:
            self.authenticity_score = authenticity_score
        if practical_score is not None:
            self.practical_application_score = practical_score
    
    def set_user_feedback(
        self,
        satisfaction: Optional[int] = None,
        difficulty: Optional[int] = None,
        time_spent: Optional[int] = None
    ) -> None:
        """Set user feedback and metadata."""
        if satisfaction is not None:
            self.user_satisfaction_rating = satisfaction
        if difficulty is not None:
            self.user_difficulty_rating = difficulty
        if time_spent is not None:
            self.time_spent_minutes = time_spent
    
    @property
    def word_count(self) -> int:
        """Get word count of the reflection text."""
        return len(self.reflection_text.split())
    
    @property
    def has_analysis(self) -> bool:
        """Check if reflection has been analyzed."""
        return any([
            self.philosophical_depth_score,
            self.complexity_score,
            self.key_insights,
            self.concepts_explored
        ])
    
    @property
    def overall_quality_score(self) -> Optional[float]:
        """Calculate overall quality score from individual metrics."""
        scores = [
            score for score in [
                self.philosophical_depth_score,
                self.complexity_score,
                self.coherence_score,
                self.authenticity_score
            ] if score is not None
        ]
        
        if not scores:
            return None
        
        return sum(scores) / len(scores)