"""Advanced philosophical AI engine with multi-tradition support."""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.nlp import nlp_pipeline
from .tradition_manager import TraditionManager

logger = logging.getLogger(__name__)


class PhilosophicalAIEngine:
    """Advanced AI engine for philosophical conversations across multiple traditions."""
    
    def __init__(self):
        """Initialize the philosophical AI engine."""
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.tradition_manager = TraditionManager()
        self.conversation_memory: Dict[str, List[Dict]] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the AI engine with all components."""
        if self._initialized:
            return
        
        logger.info("Initializing philosophical AI engine...")
        
        try:
            # Initialize NLP pipeline
            await nlp_pipeline.initialize()
            
            # Initialize tradition manager
            await self.tradition_manager.initialize()
            
            self._initialized = True
            logger.info("Philosophical AI engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI engine: {e}")
            raise
    
    async def generate_philosophical_response(
        self,
        user_message: str,
        conversation_id: str,
        user_context: Optional[Dict[str, Any]] = None,
        tradition: str = "eclectic",
        response_style: str = "socratic"
    ) -> Dict[str, Any]:
        """
        Generate a philosophical response using AI with deep context awareness.
        
        Args:
            user_message: The user's message
            conversation_id: Unique conversation identifier
            user_context: User preferences and context
            tradition: Philosophical tradition to use
            response_style: Style of response (socratic, explanatory, contemplative)
            
        Returns:
            Dictionary containing the AI response and analysis
        """
        if not self._initialized:
            await self.initialize()
        
        start_time = time.time()
        
        try:
            # Analyze user message with NLP pipeline
            user_analysis = await nlp_pipeline.analyze_text(
                user_message,
                context=user_context,
                analysis_types=["concepts", "depth", "emotions", "semantics"]
            )
            
            # Get conversation context
            conversation_context = self._get_conversation_context(conversation_id)
            
            # Build sophisticated prompt
            system_prompt = await self._build_contextual_prompt(
                tradition=tradition,
                response_style=response_style,
                user_analysis=user_analysis,
                conversation_context=conversation_context,
                user_context=user_context
            )
            
            # Prepare messages for AI
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add conversation history (last 10 messages)
            if conversation_context:
                messages.extend(conversation_context[-10:])
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate AI response
            ai_response = await self._call_openai_api(messages, tradition)
            
            # Analyze AI response
            response_analysis = await nlp_pipeline.analyze_text(
                ai_response,
                analysis_types=["concepts", "depth", "emotions"]
            )
            
            # Generate follow-up suggestions
            follow_ups = await self._generate_follow_up_questions(
                user_message, ai_response, user_analysis, tradition
            )
            
            # Update conversation memory
            self._update_conversation_memory(
                conversation_id, user_message, ai_response, user_analysis, response_analysis
            )
            
            # Calculate response time
            response_time = int((time.time() - start_time) * 1000)
            
            return {
                "response": ai_response,
                "tradition_used": tradition,
                "response_style": response_style,
                "user_analysis": {
                    "concepts": user_analysis.get("concepts", {}),
                    "depth_score": user_analysis.get("depth", {}).get("depth_score", 5),
                    "primary_emotion": user_analysis.get("emotions", {}).get("primary_emotion", "neutral"),
                    "philosophical_mood": user_analysis.get("emotions", {}).get("philosophical_mood", {})
                },
                "response_analysis": {
                    "concepts": response_analysis.get("concepts", {}),
                    "depth_score": response_analysis.get("depth", {}).get("depth_score", 5),
                    "complexity": response_analysis.get("complexity", {}).get("complexity_score", 5)
                },
                "follow_up_questions": follow_ups,
                "response_time_ms": response_time,
                "conversation_insights": await self._generate_conversation_insights(conversation_id),
                "suggested_readings": await self._suggest_related_readings(user_analysis, tradition),
                "philosophical_growth_indicators": self._identify_growth_indicators(
                    user_analysis, conversation_context
                )
            }
            
        except Exception as e:
            logger.error(f"Error generating philosophical response: {e}")
            return {
                "response": self._get_fallback_response(tradition),
                "error": str(e),
                "response_time_ms": int((time.time() - start_time) * 1000)
            }
    
    async def _build_contextual_prompt(
        self,
        tradition: str,
        response_style: str,
        user_analysis: Dict[str, Any],
        conversation_context: List[Dict],
        user_context: Optional[Dict[str, Any]]
    ) -> str:
        """Build a sophisticated, context-aware system prompt."""
        
        # Get tradition-specific prompt
        tradition_prompt = await self.tradition_manager.get_tradition_prompt(tradition)
        
        # Get style-specific guidance
        style_guidance = self._get_style_guidance(response_style)
        
        # Analyze user's philosophical sophistication
        user_depth = user_analysis.get("depth", {}).get("depth_score", 5)
        user_concepts = user_analysis.get("concepts", {}).get("concepts", [])
        user_emotion = user_analysis.get("emotions", {}).get("primary_emotion", "neutral")
        
        # Build context-aware adaptations
        sophistication_level = "advanced" if user_depth > 7 else "intermediate" if user_depth > 4 else "beginner"
        
        # Construct comprehensive prompt
        prompt = f"""{tradition_prompt}
        
{style_guidance}

CONTEXT AWARENESS:
- User's philosophical sophistication: {sophistication_level}
- Current emotional state: {user_emotion}
- Key concepts being explored: {', '.join([c.get('name', '') for c in user_concepts[:5]])}
- Conversation depth so far: {'Established dialogue' if len(conversation_context) > 2 else 'Early stage'}

ADAPTIVE RESPONSE GUIDELINES:
1. **Intellectual Level**: Match the user's demonstrated sophistication while gently encouraging deeper thinking
2. **Emotional Attunement**: Acknowledge and work with their current emotional and philosophical state
3. **Conceptual Building**: Build on concepts they've already engaged with naturally
4. **Cultural Sensitivity**: Draw from {tradition} while remaining open to other perspectives when relevant

PHILOSOPHICAL RESPONSE PRINCIPLES:
- Ask questions that deepen understanding rather than just gathering information
- Connect abstract philosophical ideas to lived human experience
- Encourage the user to think for themselves rather than providing definitive answers
- Model intellectual humility and genuine curiosity
- Help the user see connections between ideas and their personal journey
- Use examples and analogies that resonate with their demonstrated interests

CONVERSATION QUALITY:
- Maintain philosophical rigor while being approachable
- Balance challenge with support
- Show genuine interest in their unique perspective
- Encourage both rational analysis and intuitive insight
- Help them discover their own philosophical voice

Remember: You are not here to lecture or preach, but to engage in genuine philosophical dialogue that honors both the wisdom of {tradition} and the unique insights of this individual human being."""
        
        return prompt
    
    def _get_style_guidance(self, response_style: str) -> str:
        """Get style-specific response guidance."""
        styles = {
            "socratic": """
SOCRATIC STYLE:
- Lead with thoughtful questions rather than direct statements
- Help the user examine their own beliefs and assumptions
- Use gentle challenging to deepen their thinking
- Guide them to discover insights through dialogue
- Example: "What do you think might happen if we examined that belief more closely?"
            """,
            
            "explanatory": """
EXPLANATORY STYLE:
- Provide clear explanations while encouraging reflection
- Balance teaching with dialogue
- Use examples and analogies to illustrate complex concepts
- Build understanding step by step
- Example: "This connects to the idea of... What does this mean for how we might approach..."
            """,
            
            "contemplative": """
CONTEMPLATIVE STYLE:
- Encourage deep reflection and inner exploration
- Use more poetic and evocative language when appropriate
- Focus on personal meaning-making and inner wisdom
- Allow for silence, uncertainty, and mystery
- Example: "Perhaps we might sit with this question for a moment... What arises for you when you consider..."
            """
        }
        
        return styles.get(response_style, styles["socratic"])
    
    async def _call_openai_api(self, messages: List[Dict], tradition: str) -> str:
        """Make API call to OpenAI with tradition-specific parameters."""
        try:
            # Tradition-specific model parameters
            model_params = await self.tradition_manager.get_model_parameters(tradition)
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=model_params.get("temperature", 0.7),
                max_tokens=model_params.get("max_tokens", 800),
                presence_penalty=model_params.get("presence_penalty", 0.2),
                frequency_penalty=model_params.get("frequency_penalty", 0.1),
                timeout=settings.ai_response_timeout
            )
            
            return response.choices[0].message.content or "I need a moment to gather my thoughts. Could you rephrase your question?"
            
        except openai.RateLimitError:
            logger.warning("OpenAI rate limit exceeded")
            return "I'm receiving many thoughtful questions right now. Let's take a moment to reflect on our conversation so far before continuing."
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            return "I'm experiencing some difficulty formulating a response. In the spirit of philosophical inquiry, what are your own thoughts on this question?"
            
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI call: {e}")
            return self._get_fallback_response(tradition)
    
    async def _generate_follow_up_questions(
        self,
        user_message: str,
        ai_response: str,
        user_analysis: Dict[str, Any],
        tradition: str
    ) -> List[str]:
        """Generate thoughtful follow-up questions."""
        try:
            # Extract key concepts for follow-up generation
            concepts = user_analysis.get("concepts", {}).get("concepts", [])
            concept_names = [c.get("name", "") for c in concepts[:3]]
            
            # Build prompt for follow-up generation
            prompt = f"""Based on this philosophical exchange in the {tradition} tradition:

User: "{user_message[:200]}..."
Response: "{ai_response[:200]}..."

Key concepts: {', '.join(concept_names)}

Generate 3 thoughtful follow-up questions that:
1. Deepen the philosophical inquiry
2. Connect to lived experience  
3. Open new avenues of exploration

Return as a simple list, one question per line."""
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=200
            )
            
            follow_ups = response.choices[0].message.content.strip().split('\n')
            return [q.strip().lstrip('123456789.-').strip() for q in follow_ups if q.strip()][:3]
            
        except Exception as e:
            logger.error(f"Error generating follow-ups: {e}")
            return [
                "What implications does this have for how we should live?",
                "How might this connect to your own experience?",
                "What questions does this raise for you?"
            ]
    
    def _get_conversation_context(self, conversation_id: str) -> List[Dict]:
        """Get conversation context from memory."""
        return self.conversation_memory.get(conversation_id, [])
    
    def _update_conversation_memory(
        self,
        conversation_id: str,
        user_message: str,
        ai_response: str,
        user_analysis: Dict[str, Any],
        response_analysis: Dict[str, Any]
    ) -> None:
        """Update conversation memory with new exchange."""
        if conversation_id not in self.conversation_memory:
            self.conversation_memory[conversation_id] = []
        
        # Add user message
        self.conversation_memory[conversation_id].append({
            "role": "user",
            "content": user_message,
            "analysis": user_analysis
        })
        
        # Add AI response
        self.conversation_memory[conversation_id].append({
            "role": "assistant", 
            "content": ai_response,
            "analysis": response_analysis
        })
        
        # Keep only last 20 messages to manage memory
        if len(self.conversation_memory[conversation_id]) > 20:
            self.conversation_memory[conversation_id] = self.conversation_memory[conversation_id][-20:]
    
    async def _generate_conversation_insights(self, conversation_id: str) -> Dict[str, Any]:
        """Generate insights about the conversation's philosophical development."""
        context = self._get_conversation_context(conversation_id)
        
        if len(context) < 4:  # Need at least 2 exchanges
            return {"insights": [], "development_stage": "beginning"}
        
        # Analyze conversation development
        user_messages = [msg for msg in context if msg["role"] == "user"]
        
        # Track depth progression
        depth_scores = []
        for msg in user_messages:
            analysis = msg.get("analysis", {})
            depth = analysis.get("depth", {}).get("depth_score", 5)
            depth_scores.append(depth)
        
        # Calculate trends
        if len(depth_scores) >= 3:
            recent_avg = sum(depth_scores[-3:]) / 3
            early_avg = sum(depth_scores[:3]) / min(3, len(depth_scores))
            depth_trend = "deepening" if recent_avg > early_avg + 0.5 else "stable"
        else:
            depth_trend = "developing"
        
        # Extract key themes
        all_concepts = []
        for msg in user_messages:
            concepts = msg.get("analysis", {}).get("concepts", {}).get("concepts", [])
            all_concepts.extend([c.get("name", "") for c in concepts])
        
        # Find most common themes
        concept_counts = {}
        for concept in all_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        recurring_themes = [
            concept for concept, count in concept_counts.items() 
            if count >= 2
        ][:5]
        
        return {
            "development_stage": depth_trend,
            "depth_progression": depth_scores,
            "recurring_themes": recurring_themes,
            "conversation_length": len(context) // 2,  # Number of exchanges
            "insights": [
                f"The conversation shows {depth_trend} philosophical engagement",
                f"Key recurring themes: {', '.join(recurring_themes[:3]) if recurring_themes else 'diverse exploration'}"
            ]
        }
    
    async def _suggest_related_readings(
        self, 
        user_analysis: Dict[str, Any], 
        tradition: str
    ) -> List[Dict[str, str]]:
        """Suggest related readings based on user's interests and current topics."""
        concepts = user_analysis.get("concepts", {}).get("concepts", [])
        if not concepts:
            return []
        
        # Get tradition-specific recommendations
        readings = await self.tradition_manager.get_reading_suggestions(
            tradition, [c.get("name", "") for c in concepts[:3]]
        )
        
        return readings[:3]  # Return top 3 suggestions
    
    def _identify_growth_indicators(
        self, 
        user_analysis: Dict[str, Any], 
        conversation_context: List[Dict]
    ) -> List[str]:
        """Identify signs of philosophical growth and development."""
        indicators = []
        
        # Check depth score
        depth_score = user_analysis.get("depth", {}).get("depth_score", 5)
        if depth_score > 7:
            indicators.append("Demonstrates sophisticated philosophical thinking")
        
        # Check for critical analysis
        depth_analysis = user_analysis.get("depth", {})
        if depth_analysis.get("indicator_scores", {}).get("critical_analysis", 0) > 6:
            indicators.append("Shows strong critical thinking skills")
        
        # Check for synthesis
        if depth_analysis.get("synthesis_level", {}).get("synthesis_score", 0) > 6:
            indicators.append("Integrates ideas from multiple perspectives")
        
        # Check emotional sophistication
        emotions = user_analysis.get("emotions", {})
        if emotions.get("philosophical_relevance", {}).get("relevance", "") in ["high", "very_high"]:
            indicators.append("Demonstrates philosophical emotional intelligence")
        
        return indicators
    
    def _get_fallback_response(self, tradition: str) -> str:
        """Get a tradition-appropriate fallback response."""
        fallbacks = {
            "stoicism": "In the spirit of Stoicism, let us accept this moment of uncertainty and focus on what we can control - continuing our philosophical dialogue together.",
            "existentialism": "Perhaps this moment of uncertainty itself is philosophically meaningful. What does this experience of not-knowing reveal about the human condition?",
            "buddhism": "Like all phenomena, this difficulty too is impermanent. Let us return to the present moment and the question before us with mindful attention.",
            "socratic": "It seems I am reminded of Socrates' wisdom - that I know nothing. What are your own thoughts on the question you've posed?",
            "eclectic": "Philosophy often emerges from our encounters with the unexpected. What insights might we draw from this moment of uncertainty?"
        }
        
        return fallbacks.get(tradition, fallbacks["socratic"])
    
    async def analyze_philosophical_growth(
        self, 
        user_id: str, 
        time_period_days: int = 30
    ) -> Dict[str, Any]:
        """Analyze user's philosophical growth over time."""
        # This would integrate with the database to track growth
        # For now, return a structure showing what would be analyzed
        return {
            "growth_metrics": {
                "depth_progression": [],
                "concept_mastery": {},
                "critical_thinking_development": 0,
                "emotional_philosophical_intelligence": 0
            },
            "learning_recommendations": [],
            "philosophical_milestones": [],
            "areas_for_development": []
        }