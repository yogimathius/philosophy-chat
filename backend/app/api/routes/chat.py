"""Chat endpoints for philosophical conversations."""

import logging
from typing import Dict, List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Conversation, Message, User
from app.schemas.chat import (
    ChatContext,
    ChatMessage, 
    ChatResponse,
    MessageAnalysisRequest,
    MessageAnalysisResponse
)
from app.api.dependencies import get_current_user
from app.nlp import nlp_pipeline
from app.philosophy import PhilosophicalAIEngine
from app.services.conversation_service import ConversationService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message and receive philosophical AI response.
    
    This endpoint:
    - Analyzes the user's message for philosophical content
    - Generates contextually appropriate response using selected tradition
    - Tracks conversation development and user growth
    - Provides follow-up questions and reading suggestions
    """
    try:
        # Get AI engine from app state
        ai_engine: PhilosophicalAIEngine = request.app.state.ai_engine
        
        # Get or create conversation
        conversation_service = ConversationService(db)
        
        if message.conversation_id:
            conversation = await conversation_service.get_conversation(
                message.conversation_id, current_user.id
            )
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation
            conversation = await conversation_service.create_conversation(
                user_id=current_user.id,
                tradition=message.tradition,
                conversation_type="general"
            )
        
        # Update user context with preferences
        user_context = {
            "user_id": str(current_user.id),
            "learning_level": current_user.learning_level,
            "preferred_traditions": current_user.preferred_traditions,
            "philosophical_interests": current_user.philosophical_interests
        }
        
        if message.context:
            user_context.update(message.context)
        
        # Generate AI response
        ai_response = await ai_engine.generate_philosophical_response(
            user_message=message.content,
            conversation_id=str(conversation.id),
            user_context=user_context,
            tradition=message.tradition,
            response_style=message.response_style
        )
        
        # Store messages in database
        await conversation_service.add_message(
            conversation_id=conversation.id,
            sender="user",
            content=message.content,
            analysis=ai_response.get("user_analysis", {})
        )
        
        await conversation_service.add_message(
            conversation_id=conversation.id,
            sender="assistant", 
            content=ai_response["response"],
            analysis=ai_response.get("response_analysis", {}),
            ai_model_used="gpt-4-turbo-preview",
            response_time_ms=ai_response.get("response_time_ms", 0)
        )
        
        # Update conversation metadata
        await conversation_service.update_conversation_activity(conversation.id)
        
        # Update user's last active timestamp
        current_user.update_last_active()
        await db.commit()
        
        return ChatResponse(
            response=ai_response["response"],
            conversation_id=conversation.id,
            tradition_used=ai_response["tradition_used"],
            response_style=ai_response["response_style"],
            user_analysis=ai_response["user_analysis"],
            response_analysis=ai_response["response_analysis"],
            follow_up_questions=ai_response.get("follow_up_questions", []),
            response_time_ms=ai_response.get("response_time_ms", 0),
            conversation_insights=ai_response.get("conversation_insights", {}),
            suggested_readings=ai_response.get("suggested_readings", []),
            philosophical_growth_indicators=ai_response.get("philosophical_growth_indicators", [])
        )
        
    except Exception as e:
        logger.error(f"Error in chat message endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")


@router.post("/analyze", response_model=MessageAnalysisResponse)
async def analyze_message(
    analysis_request: MessageAnalysisRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Analyze a message for philosophical content without generating a response.
    
    Useful for:
    - Understanding the depth of user's philosophical thinking
    - Identifying key concepts in their message
    - Analyzing emotional and intellectual sophistication
    """
    try:
        # Perform NLP analysis
        analysis_result = await nlp_pipeline.analyze_text(
            text=analysis_request.content,
            context=analysis_request.context,
            analysis_types=analysis_request.analysis_types
        )
        
        # Create summary
        summary = {
            "overall_score": analysis_result.get("overall_scores", {}).get("overall_score", 5.0),
            "primary_concepts": [
                concept.get("name", "") 
                for concept in analysis_result.get("concepts", {}).get("concepts", [])[:5]
            ],
            "emotional_tone": analysis_result.get("emotions", {}).get("primary_emotion", "neutral"),
            "philosophical_sophistication": _categorize_sophistication(
                analysis_result.get("depth", {}).get("depth_score", 5)
            )
        }
        
        return MessageAnalysisResponse(
            analysis=analysis_result,
            summary=summary
        )
        
    except Exception as e:
        logger.error(f"Error in message analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze message")


@router.get("/context/{conversation_id}", response_model=ChatContext)
async def get_conversation_context(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get conversation context for better AI responses.
    
    Returns recent messages, user preferences, and conversation insights.
    """
    try:
        conversation_service = ConversationService(db)
        
        # Get conversation
        conversation = await conversation_service.get_conversation(
            conversation_id, current_user.id
        )
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get recent messages
        recent_messages = await conversation_service.get_recent_messages(
            conversation_id, limit=10
        )
        
        # Format conversation history
        conversation_history = [
            {
                "role": msg.sender,
                "content": msg.content
            }
            for msg in recent_messages
        ]
        
        # Get user preferences
        user_preferences = {
            "traditions": current_user.preferred_traditions,
            "learning_level": current_user.learning_level,
            "learning_style": current_user.preferred_learning_style,
            "interests": current_user.philosophical_interests
        }
        
        return ChatContext(
            user_preferences=user_preferences,
            conversation_history=conversation_history,
            current_mood=None,  # Could be enhanced with mood tracking
            learning_goals=[]   # Could be enhanced with goal tracking
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation context: {e}")
        raise HTTPException(status_code=500, detail="Failed to get context")


@router.post("/suggest-questions")
async def suggest_questions(
    message_content: str,
    tradition: str = "eclectic",
    current_user: User = Depends(get_current_user)
) -> List[str]:
    """
    Generate follow-up questions for a given message and tradition.
    
    Useful for:
    - Helping users explore topics more deeply
    - Providing conversation starters
    - Guiding philosophical inquiry
    """
    try:
        # Simple question generation based on content and tradition
        # This could be enhanced with the AI engine's question generation
        
        # Analyze the message first
        analysis = await nlp_pipeline.analyze_text(
            message_content,
            analysis_types=["concepts", "themes"]
        )
        
        concepts = analysis.get("concepts", {}).get("concepts", [])
        themes = analysis.get("themes", {}).get("themes", {})
        
        # Generate tradition-specific questions
        questions = []
        
        if tradition == "socratic":
            questions = [
                "What assumptions are we making here?",
                "How do you know this to be true?",
                "What would someone who disagrees with you say?",
                "Can you give me an example of what you mean?",
                "What are the implications of this view?"
            ]
        elif tradition == "stoicism":
            questions = [
                "What aspects of this situation are under your control?",
                "How might this challenge help you develop virtue?",
                "What would Marcus Aurelius say about this?",
                "How can you align your response with nature?",
                "What can you learn from this difficulty?"
            ]
        elif tradition == "existentialism":
            questions = [
                "What does this reveal about your freedom to choose?",
                "How are you taking responsibility for this situation?",
                "What would authentic action look like here?",
                "How are you creating meaning in this experience?",
                "What fears or anxieties does this bring up?"
            ]
        elif tradition == "buddhism":
            questions = [
                "What attachments might be causing suffering here?",
                "How can you practice compassion in this situation?",
                "What does this teach you about impermanence?",
                "How can mindfulness help you with this?",
                "What would loving-kindness look like here?"
            ]
        else:  # eclectic
            questions = [
                "How do different wisdom traditions approach this question?",
                "What would practical wisdom look like in this situation?",
                "How does this connect to your lived experience?",
                "What questions does this raise for you?",
                "How might you integrate these insights into your life?"
            ]
        
        # Return top 3-5 questions
        return questions[:5]
        
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate questions")


def _categorize_sophistication(depth_score: float) -> str:
    """Categorize philosophical sophistication level."""
    if depth_score >= 8.5:
        return "profound"
    elif depth_score >= 7:
        return "advanced"
    elif depth_score >= 5.5:
        return "intermediate"
    elif depth_score >= 4:
        return "developing"
    else:
        return "beginning"