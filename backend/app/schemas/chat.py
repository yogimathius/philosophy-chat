"""Chat-related Pydantic schemas."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class ChatMessage(BaseModel):
    """Schema for incoming chat message."""
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    conversation_id: Optional[UUID] = Field(None, description="Conversation ID (optional for new conversations)")
    tradition: str = Field("eclectic", description="Philosophical tradition to use")
    response_style: str = Field("socratic", description="Response style preference")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    
    @validator("tradition")
    def validate_tradition(cls, v):
        allowed_traditions = ["stoicism", "existentialism", "buddhism", "socratic", "eclectic"]
        if v not in allowed_traditions:
            raise ValueError(f"Tradition must be one of {allowed_traditions}")
        return v
    
    @validator("response_style")
    def validate_response_style(cls, v):
        allowed_styles = ["socratic", "explanatory", "contemplative"]
        if v not in allowed_styles:
            raise ValueError(f"Response style must be one of {allowed_styles}")
        return v


class UserAnalysis(BaseModel):
    """User message analysis results."""
    concepts: List[Dict[str, Any]] = Field(default_factory=list)
    depth_score: float = Field(..., ge=1, le=10)
    primary_emotion: str
    philosophical_mood: Dict[str, Any] = Field(default_factory=dict)


class ResponseAnalysis(BaseModel):
    """AI response analysis results."""
    concepts: List[Dict[str, Any]] = Field(default_factory=list)
    depth_score: float = Field(..., ge=1, le=10)
    complexity: float = Field(..., ge=1, le=10)


class ConversationInsights(BaseModel):
    """Conversation development insights."""
    development_stage: str
    depth_progression: List[float] = Field(default_factory=list)
    recurring_themes: List[str] = Field(default_factory=list)
    conversation_length: int = Field(..., ge=0)
    insights: List[str] = Field(default_factory=list)


class ReadingSuggestion(BaseModel):
    """Book/reading suggestion."""
    title: str
    author: str
    reason: str


class ChatResponse(BaseModel):
    """Schema for chat response."""
    response: str = Field(..., description="AI-generated philosophical response")
    conversation_id: UUID = Field(..., description="Conversation identifier")
    tradition_used: str = Field(..., description="Philosophical tradition used")
    response_style: str = Field(..., description="Response style used")
    user_analysis: UserAnalysis
    response_analysis: ResponseAnalysis
    follow_up_questions: List[str] = Field(default_factory=list, max_items=5)
    response_time_ms: int = Field(..., ge=0, description="Response generation time")
    conversation_insights: ConversationInsights
    suggested_readings: List[ReadingSuggestion] = Field(default_factory=list, max_items=3)
    philosophical_growth_indicators: List[str] = Field(default_factory=list)
    
    class Config:
        schema_extra = {
            "example": {
                "response": "What do you think it means to live a good life? As Aristotle might ask, are we talking about pleasure, virtue, or something else entirely?",
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "tradition_used": "socratic",
                "response_style": "socratic",
                "user_analysis": {
                    "concepts": [{"name": "good life", "confidence": 0.9}],
                    "depth_score": 6.5,
                    "primary_emotion": "contemplation",
                    "philosophical_mood": {"primary_mood": "wonder"}
                },
                "response_analysis": {
                    "concepts": [{"name": "virtue", "confidence": 0.8}],
                    "depth_score": 7.2,
                    "complexity": 6.8
                },
                "follow_up_questions": [
                    "What role does virtue play in your understanding of happiness?",
                    "How do you distinguish between pleasure and fulfillment?",
                    "What examples from your life illustrate a 'good life'?"
                ],
                "response_time_ms": 1250,
                "conversation_insights": {
                    "development_stage": "deepening",
                    "depth_progression": [5.2, 6.1, 6.5],
                    "recurring_themes": ["ethics", "meaning"],
                    "conversation_length": 3,
                    "insights": ["The conversation shows deepening philosophical engagement"]
                },
                "suggested_readings": [
                    {
                        "title": "Nicomachean Ethics",
                        "author": "Aristotle",
                        "reason": "Foundational work on virtue and the good life"
                    }
                ],
                "philosophical_growth_indicators": [
                    "Demonstrates sophisticated philosophical thinking"
                ]
            }
        }


class ChatContext(BaseModel):
    """Schema for chat context information."""
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User philosophical preferences")
    conversation_history: List[Dict[str, str]] = Field(default_factory=list, max_items=10)
    current_mood: Optional[str] = Field(None, description="User's current emotional state")
    learning_goals: List[str] = Field(default_factory=list, description="User's learning objectives")
    
    class Config:
        schema_extra = {
            "example": {
                "user_preferences": {
                    "traditions": ["stoicism", "buddhism"],
                    "complexity_level": "intermediate",
                    "learning_style": "socratic"
                },
                "conversation_history": [
                    {"role": "user", "content": "What is virtue?"},
                    {"role": "assistant", "content": "What do you think virtue means to you?"}
                ],
                "current_mood": "curious",
                "learning_goals": ["understand ethics", "develop practical wisdom"]
            }
        }


class MessageAnalysisRequest(BaseModel):
    """Request schema for analyzing a message without generating response."""
    content: str = Field(..., min_length=1, max_length=5000)
    analysis_types: List[str] = Field(
        default=["concepts", "depth", "emotions", "semantics"],
        description="Types of analysis to perform"
    )
    context: Optional[Dict[str, Any]] = Field(None)
    
    @validator("analysis_types")
    def validate_analysis_types(cls, v):
        allowed_types = ["concepts", "depth", "emotions", "semantics", "complexity", "coherence", "themes"]
        for analysis_type in v:
            if analysis_type not in allowed_types:
                raise ValueError(f"Analysis type '{analysis_type}' not supported. Must be one of {allowed_types}")
        return v


class MessageAnalysisResponse(BaseModel):
    """Response schema for message analysis."""
    analysis: Dict[str, Any] = Field(..., description="Complete analysis results")
    summary: Dict[str, Any] = Field(..., description="Analysis summary")
    
    class Config:
        schema_extra = {
            "example": {
                "analysis": {
                    "concepts": {
                        "concepts": [{"name": "virtue", "confidence": 0.9}]
                    },
                    "depth": {
                        "depth_score": 7.2,
                        "depth_category": "deep"
                    },
                    "emotions": {
                        "primary_emotion": "contemplation",
                        "confidence": 0.8
                    }
                },
                "summary": {
                    "overall_score": 7.0,
                    "primary_concepts": ["virtue", "ethics"],
                    "emotional_tone": "contemplative",
                    "philosophical_sophistication": "advanced"
                }
            }
        }