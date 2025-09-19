"""Daily wisdom model for philosophical insights and prompts."""

import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, Date, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


class DailyWisdom(Base):
    """Daily wisdom model for philosophical insights and prompts."""
    
    __tablename__ = "daily_wisdom"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    date = Column(Date, nullable=False, index=True)
    
    # Content
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    wisdom_type = Column(String(50), nullable=False)  # quote, question, exercise, contemplation
    
    # Source and attribution
    source = Column(String(255), nullable=True)  # Original author/text
    tradition = Column(String(100), nullable=False)  # Philosophical tradition
    historical_context = Column(Text, nullable=True)  # Background information
    
    # Classification
    difficulty_level = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    primary_theme = Column(String(100), nullable=True)  # Main philosophical theme
    concepts = Column(JSON, default=list)  # Related philosophical concepts
    tags = Column(JSON, default=list)  # Searchable tags
    
    # Engagement metadata
    estimated_reflection_time = Column(Integer, default=10)  # Minutes
    reflection_prompts = Column(JSON, default=list)  # Guided reflection questions
    follow_up_resources = Column(JSON, default=list)  # Related readings/concepts
    
    # Quality and curation
    curator_notes = Column(Text, nullable=True)  # Internal notes
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    quality_score = Column(Integer, nullable=True)  # 1-10 curation quality
    
    # Usage statistics
    view_count = Column(Integer, default=0)
    reflection_count = Column(Integer, default=0)
    average_rating = Column(Integer, nullable=True)  # Average user rating
    
    # Timestamps
    created_at = Column(Date, default=date.today, nullable=False)
    
    # Relationships
    reflections = relationship("UserReflection", back_populates="daily_wisdom")
    
    def __repr__(self) -> str:
        return f"<DailyWisdom(date={self.date}, tradition={self.tradition})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert daily wisdom to dictionary representation."""
        return {
            "id": str(self.id),
            "date": self.date.isoformat(),
            "title": self.title,
            "content": self.content,
            "wisdom_type": self.wisdom_type,
            "source": self.source,
            "tradition": self.tradition,
            "historical_context": self.historical_context,
            "difficulty_level": self.difficulty_level,
            "primary_theme": self.primary_theme,
            "concepts": self.concepts or [],
            "tags": self.tags or [],
            "estimated_reflection_time": self.estimated_reflection_time,
            "reflection_prompts": self.reflection_prompts or [],
            "follow_up_resources": self.follow_up_resources or [],
            "curator_notes": self.curator_notes,
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "quality_score": self.quality_score,
            "view_count": self.view_count,
            "reflection_count": self.reflection_count,
            "average_rating": self.average_rating,
            "created_at": self.created_at.isoformat(),
        }
    
    def add_concept(self, concept: str) -> None:
        """Add a philosophical concept to the wisdom entry."""
        concepts = self.concepts or []
        if concept not in concepts:
            concepts.append(concept)
            self.concepts = concepts
    
    def add_tag(self, tag: str) -> None:
        """Add a searchable tag to the wisdom entry."""
        tags = self.tags or []
        if tag not in tags:
            tags.append(tag)
            self.tags = tags
    
    def add_reflection_prompt(self, prompt: str) -> None:
        """Add a reflection prompt to the wisdom entry."""
        prompts = self.reflection_prompts or []
        prompts.append(prompt)
        self.reflection_prompts = prompts
    
    def add_follow_up_resource(self, resource: Dict[str, str]) -> None:
        """Add a follow-up resource (book, article, concept)."""
        resources = self.follow_up_resources or []
        resources.append(resource)
        self.follow_up_resources = resources
    
    def increment_view_count(self) -> None:
        """Increment the view count."""
        self.view_count = (self.view_count or 0) + 1
    
    def increment_reflection_count(self) -> None:
        """Increment the reflection count."""
        self.reflection_count = (self.reflection_count or 0) + 1
    
    @classmethod
    def create_quote(
        cls,
        quote_text: str,
        author: str,
        tradition: str,
        date_for: date,
        difficulty_level: str = "intermediate",
        **kwargs
    ) -> "DailyWisdom":
        """Factory method to create a quote-type wisdom entry."""
        return cls(
            date=date_for,
            content=quote_text,
            source=author,
            tradition=tradition,
            wisdom_type="quote",
            difficulty_level=difficulty_level,
            **kwargs
        )
    
    @classmethod
    def create_question(
        cls,
        question_text: str,
        tradition: str,
        date_for: date,
        context: Optional[str] = None,
        difficulty_level: str = "intermediate",
        **kwargs
    ) -> "DailyWisdom":
        """Factory method to create a question-type wisdom entry."""
        return cls(
            date=date_for,
            content=question_text,
            tradition=tradition,
            wisdom_type="question",
            historical_context=context,
            difficulty_level=difficulty_level,
            **kwargs
        )
    
    @classmethod
    def create_exercise(
        cls,
        exercise_text: str,
        tradition: str,
        date_for: date,
        estimated_time: int = 15,
        difficulty_level: str = "intermediate",
        **kwargs
    ) -> "DailyWisdom":
        """Factory method to create an exercise-type wisdom entry."""
        return cls(
            date=date_for,
            content=exercise_text,
            tradition=tradition,
            wisdom_type="exercise",
            estimated_reflection_time=estimated_time,
            difficulty_level=difficulty_level,
            **kwargs
        )
    
    @property
    def is_quote(self) -> bool:
        """Check if this is a quote-type wisdom entry."""
        return self.wisdom_type == "quote"
    
    @property
    def is_question(self) -> bool:
        """Check if this is a question-type wisdom entry."""
        return self.wisdom_type == "question"
    
    @property
    def is_exercise(self) -> bool:
        """Check if this is an exercise-type wisdom entry."""
        return self.wisdom_type == "exercise"
    
    @property
    def formatted_content(self) -> str:
        """Get formatted content based on wisdom type."""
        if self.is_quote and self.source:
            return f'"{self.content}"\n\n— {self.source}'
        return self.content