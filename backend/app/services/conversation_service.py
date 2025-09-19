"""Service for conversation management and database operations."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Conversation, Message, User

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for managing conversations and messages."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_conversation(
        self,
        user_id: UUID,
        tradition: str,
        conversation_type: str = "general",
        title: Optional[str] = None,
        theme: Optional[str] = None
    ) -> Conversation:
        """Create a new conversation."""
        try:
            conversation = Conversation(
                user_id=user_id,
                title=title or f"{tradition.title()} Discussion",
                philosophical_tradition=tradition,
                conversation_type=conversation_type,
                theme=theme
            )
            
            self.db.add(conversation)
            await self.db.commit()
            await self.db.refresh(conversation)
            
            logger.info(f"Created conversation {conversation.id} for user {user_id}")
            return conversation
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating conversation: {e}")
            raise
    
    async def get_conversation(
        self, 
        conversation_id: UUID, 
        user_id: UUID
    ) -> Optional[Conversation]:
        """Get a conversation by ID, ensuring it belongs to the user."""
        try:
            result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                .options(selectinload(Conversation.messages))
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Error getting conversation {conversation_id}: {e}")
            return None
    
    async def get_user_conversations(
        self,
        user_id: UUID,
        limit: int = 50,
        offset: int = 0,
        include_archived: bool = False
    ) -> List[Conversation]:
        """Get user's conversations with pagination."""
        try:
            query = (
                select(Conversation)
                .where(Conversation.user_id == user_id)
                .order_by(desc(Conversation.last_activity))
                .limit(limit)
                .offset(offset)
            )
            
            if not include_archived:
                query = query.where(Conversation.is_archived == False)
            
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error getting user conversations: {e}")
            return []
    
    async def add_message(
        self,
        conversation_id: UUID,
        sender: str,
        content: str,
        analysis: Optional[Dict[str, Any]] = None,
        ai_model_used: Optional[str] = None,
        response_time_ms: Optional[int] = None
    ) -> Message:
        """Add a message to a conversation."""
        try:
            message = Message(
                conversation_id=conversation_id,
                sender=sender,
                content=content
            )
            
            # Add analysis results if provided
            if analysis:
                concepts = analysis.get("concepts", {}).get("concepts", [])
                message.philosophical_concepts = concepts
                
                depth_analysis = analysis.get("depth", {})
                message.complexity_score = int(depth_analysis.get("depth_score", 5))
                message.depth_indicators = depth_analysis.get("depth_markers", [])
                
                emotions = analysis.get("emotions", {})
                message.emotional_tone = emotions.get("primary_emotion", "neutral")
            
            # Add AI metadata for assistant messages
            if sender == "assistant":
                message.ai_model_used = ai_model_used
                message.response_time_ms = response_time_ms
            
            self.db.add(message)
            await self.db.commit()
            await self.db.refresh(message)
            
            return message
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error adding message: {e}")
            raise
    
    async def get_recent_messages(
        self,
        conversation_id: UUID,
        limit: int = 10
    ) -> List[Message]:
        """Get recent messages from a conversation."""
        try:
            result = await self.db.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(desc(Message.created_at))
                .limit(limit)
            )
            messages = result.scalars().all()
            return list(reversed(messages))  # Return in chronological order
            
        except Exception as e:
            logger.error(f"Error getting recent messages: {e}")
            return []
    
    async def update_conversation_activity(self, conversation_id: UUID) -> None:
        """Update conversation's last activity timestamp."""
        try:
            result = await self.db.execute(
                select(Conversation).where(Conversation.id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            
            if conversation:
                conversation.update_activity()
                await self.db.commit()
                
        except Exception as e:
            logger.error(f"Error updating conversation activity: {e}")
    
    async def update_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
        **updates
    ) -> Optional[Conversation]:
        """Update conversation properties."""
        try:
            result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            )
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                return None
            
            # Update allowed fields
            allowed_fields = [
                'title', 'summary', 'philosophical_tradition', 
                'conversation_type', 'theme', 'is_archived'
            ]
            
            for field, value in updates.items():
                if field in allowed_fields:
                    setattr(conversation, field, value)
            
            await self.db.commit()
            await self.db.refresh(conversation)
            
            return conversation
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating conversation: {e}")
            return None
    
    async def delete_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID
    ) -> bool:
        """Delete a conversation and all its messages."""
        try:
            result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            )
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                return False
            
            await self.db.delete(conversation)
            await self.db.commit()
            
            logger.info(f"Deleted conversation {conversation_id}")
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting conversation: {e}")
            return False
    
    async def archive_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID
    ) -> bool:
        """Archive a conversation."""
        try:
            result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            )
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                return False
            
            conversation.is_archived = True
            await self.db.commit()
            
            return True
            
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error archiving conversation: {e}")
            return False
    
    async def get_conversation_analytics(
        self,
        user_id: UUID,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """Get conversation analytics for a user."""
        try:
            # Get conversations from the specified period
            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            
            result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.user_id == user_id,
                    Conversation.created_at >= cutoff_date
                )
                .options(selectinload(Conversation.messages))
            )
            conversations = result.scalars().all()
            
            if not conversations:
                return {
                    "total_conversations": 0,
                    "total_messages": 0,
                    "avg_messages_per_conversation": 0,
                    "favorite_traditions": [],
                    "conversation_types": {},
                    "depth_trend": []
                }
            
            # Calculate analytics
            total_conversations = len(conversations)
            total_messages = sum(len(conv.messages) for conv in conversations)
            avg_messages = total_messages / total_conversations if total_conversations > 0 else 0
            
            # Tradition preferences
            tradition_counts = {}
            for conv in conversations:
                tradition = conv.philosophical_tradition or "unknown"
                tradition_counts[tradition] = tradition_counts.get(tradition, 0) + 1
            
            favorite_traditions = sorted(
                tradition_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
            
            # Conversation types
            type_counts = {}
            for conv in conversations:
                conv_type = conv.conversation_type or "general"
                type_counts[conv_type] = type_counts.get(conv_type, 0) + 1
            
            # Depth trend (simplified - would need message analysis in real implementation)
            depth_trend = []
            for conv in conversations:
                user_messages = [m for m in conv.messages if m.sender == "user"]
                if user_messages:
                    avg_complexity = sum(
                        m.complexity_score or 5 for m in user_messages
                    ) / len(user_messages)
                    depth_trend.append({
                        "date": conv.created_at.isoformat(),
                        "depth_score": avg_complexity
                    })
            
            return {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "avg_messages_per_conversation": round(avg_messages, 1),
                "favorite_traditions": [{"tradition": t, "count": c} for t, c in favorite_traditions],
                "conversation_types": type_counts,
                "depth_trend": depth_trend
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation analytics: {e}")
            return {}
    
    async def search_conversations(
        self,
        user_id: UUID,
        query: str,
        limit: int = 20
    ) -> List[Conversation]:
        """Search user's conversations by content."""
        try:
            # Simple text search - could be enhanced with full-text search
            result = await self.db.execute(
                select(Conversation)
                .where(
                    Conversation.user_id == user_id,
                    Conversation.title.ilike(f"%{query}%") |
                    Conversation.summary.ilike(f"%{query}%")
                )
                .order_by(desc(Conversation.last_activity))
                .limit(limit)
            )
            
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Error searching conversations: {e}")
            return []