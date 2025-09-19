"""Philosophical concept model for knowledge base."""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.core.database import Base


class PhilosophicalConcept(Base):
    """Philosophical concept model for building knowledge base."""
    
    __tablename__ = "philosophical_concepts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Core concept information
    name = Column(String(255), unique=True, nullable=False, index=True)
    alternative_names = Column(JSON, default=list)  # Synonyms and alternative terms
    definition = Column(Text, nullable=False)
    etymology = Column(Text, nullable=True)  # Word origin and history
    
    # Categorization
    tradition = Column(String(100), nullable=False, index=True)  # Primary tradition
    related_traditions = Column(JSON, default=list)  # Other relevant traditions
    category = Column(String(100), nullable=True)  # ethics, metaphysics, epistemology, etc.
    subcategory = Column(String(100), nullable=True)  # More specific classification
    
    # Relationships and connections
    key_thinkers = Column(JSON, default=list)  # Associated philosophers
    related_concepts = Column(JSON, default=list)  # Related concept IDs or names
    opposing_concepts = Column(JSON, default=list)  # Contrasting concepts
    prerequisite_concepts = Column(JSON, default=list)  # Concepts to understand first
    
    # Educational metadata
    difficulty_level = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    complexity_score = Column(Integer, nullable=True)  # 1-10 complexity rating
    historical_importance = Column(Integer, nullable=True)  # 1-10 historical significance
    contemporary_relevance = Column(Integer, nullable=True)  # 1-10 modern relevance
    
    # Content and examples
    examples = Column(JSON, default=list)  # Real-world examples and applications
    common_misconceptions = Column(JSON, default=list)  # Frequent misunderstandings
    key_questions = Column(JSON, default=list)  # Questions this concept addresses
    practical_applications = Column(JSON, default=list)  # How to apply in daily life
    
    # Resources and further reading
    primary_sources = Column(JSON, default=list)  # Original philosophical texts
    secondary_sources = Column(JSON, default=list)  # Scholarly commentary
    recommended_readings = Column(JSON, default=list)  # Accessible introductions
    related_media = Column(JSON, default=list)  # Videos, podcasts, etc.
    
    # Usage and quality metrics
    usage_count = Column(Integer, default=0)  # How often referenced
    user_ratings = Column(JSON, default=list)  # User feedback on explanations
    expert_reviewed = Column(Boolean, default=False)  # Professional review status
    last_updated_by = Column(String(255), nullable=True)  # Editor information
    
    # Linguistic and NLP data
    semantic_tags = Column(JSON, default=list)  # Tags for semantic matching
    nlp_embeddings = Column(JSON, nullable=True)  # Vector embeddings for similarity
    common_contexts = Column(JSON, default=list)  # Typical usage contexts
    
    # Status and curation
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)  # Highlighted for learning paths
    review_status = Column(String(50), default="pending")  # pending, reviewed, approved
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<PhilosophicalConcept(name={self.name}, tradition={self.tradition})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert concept to dictionary representation."""
        return {
            "id": str(self.id),
            "name": self.name,
            "alternative_names": self.alternative_names or [],
            "definition": self.definition,
            "etymology": self.etymology,
            "tradition": self.tradition,
            "related_traditions": self.related_traditions or [],
            "category": self.category,
            "subcategory": self.subcategory,
            "key_thinkers": self.key_thinkers or [],
            "related_concepts": self.related_concepts or [],
            "opposing_concepts": self.opposing_concepts or [],
            "prerequisite_concepts": self.prerequisite_concepts or [],
            "difficulty_level": self.difficulty_level,
            "complexity_score": self.complexity_score,
            "historical_importance": self.historical_importance,
            "contemporary_relevance": self.contemporary_relevance,
            "examples": self.examples or [],
            "common_misconceptions": self.common_misconceptions or [],
            "key_questions": self.key_questions or [],
            "practical_applications": self.practical_applications or [],
            "primary_sources": self.primary_sources or [],
            "secondary_sources": self.secondary_sources or [],
            "recommended_readings": self.recommended_readings or [],
            "related_media": self.related_media or [],
            "usage_count": self.usage_count,
            "user_ratings": self.user_ratings or [],
            "expert_reviewed": self.expert_reviewed,
            "last_updated_by": self.last_updated_by,
            "semantic_tags": self.semantic_tags or [],
            "common_contexts": self.common_contexts or [],
            "is_active": self.is_active,
            "is_featured": self.is_featured,
            "review_status": self.review_status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def add_alternative_name(self, name: str) -> None:
        """Add an alternative name/synonym."""
        alternatives = self.alternative_names or []
        if name not in alternatives:
            alternatives.append(name)
            self.alternative_names = alternatives
    
    def add_thinker(self, thinker: str, relationship: Optional[str] = None) -> None:
        """Add a key thinker associated with this concept."""
        thinkers = self.key_thinkers or []
        thinker_entry = {"name": thinker}
        if relationship:
            thinker_entry["relationship"] = relationship
        thinkers.append(thinker_entry)
        self.key_thinkers = thinkers
    
    def add_related_concept(self, concept: str, relationship_type: str = "related") -> None:
        """Add a related concept."""
        related = self.related_concepts or []
        related.append({
            "name": concept,
            "relationship": relationship_type,
            "added_at": datetime.utcnow().isoformat()
        })
        self.related_concepts = related
    
    def add_example(self, example: str, context: Optional[str] = None) -> None:
        """Add a practical example."""
        examples = self.examples or []
        example_entry = {"description": example}
        if context:
            example_entry["context"] = context
        examples.append(example_entry)
        self.examples = examples
    
    def add_misconception(self, misconception: str, correction: str) -> None:
        """Add a common misconception and its correction."""
        misconceptions = self.common_misconceptions or []
        misconceptions.append({
            "misconception": misconception,
            "correction": correction,
            "added_at": datetime.utcnow().isoformat()
        })
        self.common_misconceptions = misconceptions
    
    def add_question(self, question: str) -> None:
        """Add a key question this concept addresses."""
        questions = self.key_questions or []
        questions.append(question)
        self.key_questions = questions
    
    def add_practical_application(self, application: str, context: Optional[str] = None) -> None:
        """Add a practical application."""
        applications = self.practical_applications or []
        app_entry = {"description": application}
        if context:
            app_entry["context"] = context
        applications.append(app_entry)
        self.practical_applications = applications
    
    def add_reading(self, title: str, author: str, reading_type: str = "secondary") -> None:
        """Add a reading recommendation."""
        reading_entry = {
            "title": title,
            "author": author,
            "added_at": datetime.utcnow().isoformat()
        }
        
        if reading_type == "primary":
            readings = self.primary_sources or []
            readings.append(reading_entry)
            self.primary_sources = readings
        elif reading_type == "secondary":
            readings = self.secondary_sources or []
            readings.append(reading_entry)
            self.secondary_sources = readings
        else:  # recommended
            readings = self.recommended_readings or []
            readings.append(reading_entry)
            self.recommended_readings = readings
    
    def add_semantic_tag(self, tag: str) -> None:
        """Add a semantic tag for NLP matching."""
        tags = self.semantic_tags or []
        if tag not in tags:
            tags.append(tag)
            self.semantic_tags = tags
    
    def increment_usage(self) -> None:
        """Increment usage count."""
        self.usage_count = (self.usage_count or 0) + 1
    
    def add_user_rating(self, rating: int, comment: Optional[str] = None) -> None:
        """Add user rating (1-5 stars)."""
        ratings = self.user_ratings or []
        rating_entry = {
            "rating": rating,
            "timestamp": datetime.utcnow().isoformat()
        }
        if comment:
            rating_entry["comment"] = comment
        ratings.append(rating_entry)
        self.user_ratings = ratings
    
    @property
    def average_rating(self) -> Optional[float]:
        """Calculate average user rating."""
        if not self.user_ratings:
            return None
        ratings = [r.get("rating", 0) for r in self.user_ratings if "rating" in r]
        return sum(ratings) / len(ratings) if ratings else None
    
    @property
    def all_names(self) -> List[str]:
        """Get all names including alternatives."""
        names = [self.name]
        if self.alternative_names:
            names.extend(self.alternative_names)
        return names
    
    @classmethod
    def create_with_basics(
        cls,
        name: str,
        definition: str,
        tradition: str,
        difficulty_level: str = "intermediate"
    ) -> "PhilosophicalConcept":
        """Factory method to create concept with basic information."""
        return cls(
            name=name,
            definition=definition,
            tradition=tradition,
            difficulty_level=difficulty_level
        )