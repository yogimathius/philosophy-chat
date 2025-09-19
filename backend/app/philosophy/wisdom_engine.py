"""Wisdom engine for daily philosophical insights and reflection analysis."""

import asyncio
import logging
import random
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DailyWisdom, User, UserReflection
from app.nlp import nlp_pipeline

logger = logging.getLogger(__name__)


class WisdomEngine:
    """Engine for generating daily wisdom and analyzing user reflections."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.wisdom_database = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize wisdom engine with curated content."""
        if self._initialized:
            return
        
        logger.info("Initializing wisdom engine...")
        
        try:
            await self._load_wisdom_database()
            self._initialized = True
            logger.info("Wisdom engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize wisdom engine: {e}")
            raise
    
    async def _load_wisdom_database(self) -> None:
        """Load curated philosophical wisdom content."""
        
        self.wisdom_database = {
            "stoicism": {
                "quotes": [
                    {
                        "content": "You have power over your mind - not outside events. Realize this, and you will find strength.",
                        "source": "Marcus Aurelius, Meditations",
                        "concepts": ["control", "inner_strength", "perception"],
                        "reflection_prompts": [
                            "What aspects of your current situation are within your control?",
                            "How might focusing on what you can control change your perspective?",
                            "What would it feel like to fully accept what you cannot change?"
                        ]
                    },
                    {
                        "content": "It's not what happens to you, but how you react to it that matters.",
                        "source": "Epictetus, Discourses",
                        "concepts": ["response", "choice", "resilience"],
                        "reflection_prompts": [
                            "Think of a recent challenging situation. How did you respond?",
                            "What would a wise response have looked like?",
                            "How can you prepare yourself for future challenges?"
                        ]
                    },
                    {
                        "content": "The best revenge is not to be like your enemy.",
                        "source": "Marcus Aurelius, Meditations",
                        "concepts": ["virtue", "character", "integrity"],
                        "reflection_prompts": [
                            "How do you maintain your integrity when others don't?",
                            "What does it mean to 'be the bigger person'?",
                            "How does responding with virtue benefit you?"
                        ]
                    }
                ],
                
                "questions": [
                    {
                        "content": "What would it mean to live according to your highest values today?",
                        "concepts": ["virtue", "values", "practical_ethics"],
                        "context": "Stoics believed in living according to virtue and our highest nature as rational beings.",
                        "reflection_prompts": [
                            "What are your core values?",
                            "How do these values guide your daily decisions?",
                            "Where might you be compromising your values?"
                        ]
                    },
                    {
                        "content": "If today were your last day, how would you choose to spend it?",
                        "concepts": ["mortality", "priorities", "meaning"],
                        "context": "Memento mori - remembering death helps us focus on what truly matters.",
                        "reflection_prompts": [
                            "What activities would you prioritize?",
                            "What relationships deserve your attention?",
                            "What would you want to be remembered for?"
                        ]
                    }
                ],
                
                "exercises": [
                    {
                        "content": "Practice the discipline of perception: For the next challenging situation you encounter, pause and ask yourself: 'What is actually happening here?' vs 'What story am I telling myself about what's happening?'",
                        "concepts": ["perception", "objectivity", "mindfulness"],
                        "estimated_time": 5,
                        "reflection_prompts": [
                            "What did you notice about your initial reaction?",
                            "How did separating facts from interpretation help?",
                            "What patterns do you notice in your thinking?"
                        ]
                    }
                ]
            },
            
            "existentialism": {
                "quotes": [
                    {
                        "content": "In anguish, man becomes aware of his freedom.",
                        "source": "Jean-Paul Sartre, Being and Nothingness",
                        "concepts": ["freedom", "responsibility", "anxiety"],
                        "reflection_prompts": [
                            "When do you feel most aware of your freedom to choose?",
                            "What choices are you avoiding due to anxiety?",
                            "How does recognizing your freedom change your perspective?"
                        ]
                    },
                    {
                        "content": "We are our choices.",
                        "source": "Jean-Paul Sartre",
                        "concepts": ["authenticity", "responsibility", "identity"],
                        "reflection_prompts": [
                            "What do your recent choices say about who you are?",
                            "Are you choosing based on your authentic self or others' expectations?",
                            "What would you choose if no one was watching?"
                        ]
                    }
                ],
                
                "questions": [
                    {
                        "content": "What would it mean to live authentically in your current circumstances?",
                        "concepts": ["authenticity", "bad_faith", "genuine_self"],
                        "context": "Existentialists emphasize the importance of being true to oneself rather than conforming to social roles.",
                        "reflection_prompts": [
                            "Where in your life do you feel most authentic?",
                            "What social roles or expectations constrain you?",
                            "What would change if you prioritized authenticity?"
                        ]
                    }
                ],
                
                "exercises": [
                    {
                        "content": "Freedom recognition exercise: Before making your next significant decision, pause and say 'I am radically free to choose, and I alone am responsible for this choice.' Notice how this feels.",
                        "concepts": ["freedom", "responsibility", "choice"],
                        "estimated_time": 10,
                        "reflection_prompts": [
                            "How did acknowledging your freedom feel?",
                            "What resistance did you notice?",
                            "How does accepting responsibility change your relationship to the choice?"
                        ]
                    }
                ]
            },
            
            "buddhism": {
                "quotes": [
                    {
                        "content": "The root of suffering is attachment.",
                        "source": "Buddhist Teaching",
                        "concepts": ["attachment", "suffering", "letting_go"],
                        "reflection_prompts": [
                            "What are you most attached to right now?",
                            "How does this attachment create suffering?",
                            "What would it feel like to hold this more lightly?"
                        ]
                    },
                    {
                        "content": "Be where you are; otherwise you will miss your life.",
                        "source": "Buddha",
                        "concepts": ["mindfulness", "presence", "awareness"],
                        "reflection_prompts": [
                            "How often is your mind truly present?",
                            "What takes you away from the present moment?",
                            "What do you notice when you're fully here?"
                        ]
                    }
                ],
                
                "questions": [
                    {
                        "content": "What would it mean to respond to today's challenges with compassion rather than reactivity?",
                        "concepts": ["compassion", "mindfulness", "response"],
                        "context": "Buddhism teaches that we can respond to difficulties with wisdom and compassion rather than reactive patterns.",
                        "reflection_prompts": [
                            "What triggers your reactive patterns?",
                            "How might compassion change your responses?",
                            "What would self-compassion look like today?"
                        ]
                    }
                ],
                
                "exercises": [
                    {
                        "content": "Impermanence meditation: Spend 10 minutes observing your thoughts, emotions, and sensations. Notice how everything changes and flows. Nothing remains the same.",
                        "concepts": ["impermanence", "meditation", "awareness"],
                        "estimated_time": 10,
                        "reflection_prompts": [
                            "What did you notice about the changing nature of experience?",
                            "How does recognizing impermanence affect your relationship to difficult emotions?",
                            "What insights arose during this practice?"
                        ]
                    }
                ]
            }
        }
    
    async def get_daily_wisdom(
        self, 
        user: User, 
        target_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """Get or generate daily wisdom for a user."""
        if not self._initialized:
            await self.initialize()
        
        target_date = target_date or date.today()
        
        try:
            # Check if wisdom already exists for this date
            result = await self.db.execute(
                select(DailyWisdom).where(DailyWisdom.date == target_date)
            )
            existing_wisdom = result.scalar_one_or_none()
            
            if existing_wisdom:
                return await self._format_wisdom_response(existing_wisdom, user)
            
            # Generate new daily wisdom
            wisdom_entry = await self._generate_daily_wisdom(user, target_date)
            
            if wisdom_entry:
                self.db.add(wisdom_entry)
                await self.db.commit()
                await self.db.refresh(wisdom_entry)
                
                return await self._format_wisdom_response(wisdom_entry, user)
            else:
                # Fallback wisdom
                return await self._get_fallback_wisdom(user)
                
        except Exception as e:
            logger.error(f"Error getting daily wisdom: {e}")
            return await self._get_fallback_wisdom(user)
    
    async def _generate_daily_wisdom(
        self, 
        user: User, 
        target_date: date
    ) -> Optional[DailyWisdom]:
        """Generate new daily wisdom based on user preferences."""
        try:
            # Get user's preferred traditions
            preferred_traditions = user.preferred_traditions
            if not preferred_traditions:
                preferred_traditions = ["stoicism", "buddhism", "existentialism"]
            
            # Select a tradition for today
            selected_tradition = random.choice(preferred_traditions)
            tradition_data = self.wisdom_database.get(selected_tradition, {})
            
            # Select wisdom type based on user's learning style
            wisdom_types = ["quotes", "questions", "exercises"]
            if user.preferred_learning_style == "contemplative":
                wisdom_types = ["quotes", "exercises"]  # Prefer reflective content
            elif user.preferred_learning_style == "socratic":
                wisdom_types = ["questions", "quotes"]  # Prefer questioning
            
            # Select content
            selected_type = random.choice(wisdom_types)
            type_content = tradition_data.get(selected_type, [])
            
            if not type_content:
                return None
            
            selected_content = random.choice(type_content)
            
            # Create wisdom entry
            wisdom = DailyWisdom(
                date=target_date,
                tradition=selected_tradition,
                wisdom_type=selected_type.rstrip('s'),  # Remove plural
                content=selected_content["content"],
                source=selected_content.get("source", f"{selected_tradition.title()} Teaching"),
                concepts=selected_content.get("concepts", []),
                difficulty_level=user.learning_level,
                reflection_prompts=selected_content.get("reflection_prompts", []),
                estimated_reflection_time=selected_content.get("estimated_time", 15)
            )
            
            return wisdom
            
        except Exception as e:
            logger.error(f"Error generating daily wisdom: {e}")
            return None
    
    async def _format_wisdom_response(
        self, 
        wisdom: DailyWisdom, 
        user: User
    ) -> Dict[str, Any]:
        """Format wisdom entry for response."""
        try:
            # Increment view count
            wisdom.increment_view_count()
            await self.db.commit()
            
            # Get related concepts if available
            related_concepts = []
            if wisdom.concepts:
                # This could be enhanced to fetch from philosophical concept database
                related_concepts = wisdom.concepts[:3]
            
            return {
                "id": str(wisdom.id),
                "date": wisdom.date.isoformat(),
                "tradition": wisdom.tradition,
                "type": wisdom.wisdom_type,
                "content": wisdom.formatted_content,
                "source": wisdom.source,
                "concepts": wisdom.concepts or [],
                "reflection_prompts": wisdom.reflection_prompts or [],
                "estimated_time_minutes": wisdom.estimated_reflection_time,
                "difficulty_level": wisdom.difficulty_level,
                "related_concepts": related_concepts,
                "user_context": {
                    "learning_level": user.learning_level,
                    "preferred_traditions": user.preferred_traditions,
                    "learning_style": user.preferred_learning_style
                }
            }
            
        except Exception as e:
            logger.error(f"Error formatting wisdom response: {e}")
            return {}
    
    async def process_user_reflection(
        self,
        user_id: str,
        wisdom_id: str,
        reflection_text: str,
        time_spent: Optional[int] = None
    ) -> Dict[str, Any]:
        """Process and analyze user reflection on daily wisdom."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Analyze reflection with NLP pipeline
            analysis = await nlp_pipeline.analyze_text(
                reflection_text,
                analysis_types=["concepts", "depth", "emotions", "complexity"]
            )
            
            # Calculate philosophical depth score
            depth_score = analysis.get("depth", {}).get("depth_score", 5)
            
            # Extract key insights
            key_insights = await self._extract_reflection_insights(
                reflection_text, analysis
            )
            
            # Identify growth indicators
            growth_indicators = await self._identify_growth_patterns(
                user_id, reflection_text, analysis
            )
            
            # Create reflection entry
            reflection = UserReflection(
                user_id=user_id,
                daily_wisdom_id=wisdom_id,
                reflection_text=reflection_text,
                philosophical_depth_score=int(depth_score),
                complexity_score=analysis.get("complexity", {}).get("complexity_score", 5),
                emotional_tone=analysis.get("emotions", {}).get("primary_emotion", "neutral"),
                key_insights=key_insights,
                concepts_explored=analysis.get("concepts", {}).get("concepts", []),
                growth_indicators=growth_indicators,
                time_spent_minutes=time_spent
            )
            
            self.db.add(reflection)
            await self.db.commit()
            await self.db.refresh(reflection)
            
            # Generate personalized feedback
            feedback = await self._generate_reflection_feedback(reflection, analysis)
            
            # Update wisdom reflection count
            await self._update_wisdom_stats(wisdom_id)
            
            return {
                "reflection_id": str(reflection.id),
                "analysis": {
                    "depth_score": depth_score,
                    "complexity_score": analysis.get("complexity", {}).get("complexity_score", 5),
                    "emotional_tone": analysis.get("emotions", {}).get("primary_emotion", "neutral"),
                    "philosophical_mood": analysis.get("emotions", {}).get("philosophical_mood", {}),
                    "key_concepts": [c.get("name", "") for c in analysis.get("concepts", {}).get("concepts", [])[:5]]
                },
                "insights": key_insights,
                "growth_indicators": growth_indicators,
                "personalized_feedback": feedback,
                "follow_up_suggestions": await self._suggest_follow_up_explorations(
                    reflection_text, analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Error processing reflection: {e}")
            raise
    
    async def _extract_reflection_insights(
        self, 
        reflection_text: str, 
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract key insights from reflection."""
        insights = []
        
        # Look for personal connections
        personal_indicators = [
            "i feel", "i think", "i realize", "i understand", "i notice",
            "this reminds me", "in my experience", "for me", "i've learned"
        ]
        
        text_lower = reflection_text.lower()
        for indicator in personal_indicators:
            if indicator in text_lower:
                insights.append({
                    "type": "personal_connection",
                    "indicator": indicator,
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        # Look for questions raised
        questions = [s for s in reflection_text.split('.') if '?' in s]
        for question in questions[:3]:  # Limit to first 3 questions
            insights.append({
                "type": "question_raised",
                "content": question.strip(),
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Look for practical applications
        application_indicators = [
            "i will", "i plan to", "i want to", "i should", "i need to",
            "next time", "going forward", "i commit to"
        ]
        
        for indicator in application_indicators:
            if indicator in text_lower:
                insights.append({
                    "type": "practical_application",
                    "indicator": indicator,
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return insights[:10]  # Limit total insights
    
    async def _identify_growth_patterns(
        self, 
        user_id: str, 
        reflection_text: str, 
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify signs of philosophical growth."""
        growth_indicators = []
        
        # Check depth progression
        depth_score = analysis.get("depth", {}).get("depth_score", 5)
        if depth_score > 7:
            growth_indicators.append({
                "type": "sophisticated_thinking",
                "description": "Demonstrates advanced philosophical reasoning",
                "score": depth_score
            })
        
        # Check for critical thinking
        depth_analysis = analysis.get("depth", {})
        critical_score = depth_analysis.get("indicator_scores", {}).get("critical_analysis", 0)
        if critical_score > 6:
            growth_indicators.append({
                "type": "critical_analysis",
                "description": "Shows strong critical examination of ideas",
                "score": critical_score
            })
        
        # Check for synthesis
        synthesis_score = depth_analysis.get("synthesis_level", {}).get("synthesis_score", 0)
        if synthesis_score > 6:
            growth_indicators.append({
                "type": "conceptual_integration",
                "description": "Integrates multiple philosophical perspectives",
                "score": synthesis_score
            })
        
        # Check emotional sophistication
        emotions = analysis.get("emotions", {})
        phil_relevance = emotions.get("philosophical_relevance", {}).get("relevance", "")
        if phil_relevance in ["high", "very_high"]:
            growth_indicators.append({
                "type": "philosophical_emotional_intelligence",
                "description": "Demonstrates philosophical emotional sophistication"
            })
        
        return growth_indicators
    
    async def _generate_reflection_feedback(
        self, 
        reflection: UserReflection, 
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate personalized feedback on reflection."""
        feedback = {
            "encouragement": [],
            "suggestions": [],
            "next_steps": []
        }
        
        # Encouragement based on depth
        if reflection.philosophical_depth_score >= 8:
            feedback["encouragement"].append("Your reflection demonstrates profound philosophical thinking.")
        elif reflection.philosophical_depth_score >= 6:
            feedback["encouragement"].append("You're engaging deeply with these philosophical ideas.")
        else:
            feedback["encouragement"].append("Thank you for taking time to reflect on these ideas.")
        
        # Suggestions for improvement
        if reflection.philosophical_depth_score < 6:
            feedback["suggestions"].append("Try connecting these ideas to specific examples from your own life.")
            feedback["suggestions"].append("Consider what questions this raises for you.")
        
        # Next steps based on concepts explored
        concepts = analysis.get("concepts", {}).get("concepts", [])
        if concepts:
            concept_names = [c.get("name", "") for c in concepts[:2]]
            feedback["next_steps"].append(
                f"Continue exploring: {', '.join(concept_names)}"
            )
        
        return feedback
    
    async def _suggest_follow_up_explorations(
        self, 
        reflection_text: str, 
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Suggest follow-up explorations based on reflection."""
        suggestions = []
        
        # Based on emotional tone
        emotion = analysis.get("emotions", {}).get("primary_emotion", "neutral")
        
        if emotion in ["wonder", "curiosity"]:
            suggestions.append("Explore this curiosity through additional reading or contemplation")
        elif emotion in ["anxiety", "uncertainty"]:
            suggestions.append("Practice sitting with uncertainty as a doorway to wisdom")
        elif emotion in ["inspiration", "joy"]:
            suggestions.append("Consider how to integrate this inspiration into daily action")
        
        # Based on concepts
        concepts = analysis.get("concepts", {}).get("concepts", [])
        if concepts:
            suggestions.append(
                f"Deepen your understanding through meditation on: {concepts[0].get('name', 'this concept')}"
            )
        
        # General suggestions
        suggestions.extend([
            "Journal about how this applies to a current life situation",
            "Discuss these insights with a trusted friend or mentor",
            "Create a specific practice based on this reflection"
        ])
        
        return suggestions[:5]
    
    async def _update_wisdom_stats(self, wisdom_id: str) -> None:
        """Update wisdom entry statistics."""
        try:
            result = await self.db.execute(
                select(DailyWisdom).where(DailyWisdom.id == wisdom_id)
            )
            wisdom = result.scalar_one_or_none()
            
            if wisdom:
                wisdom.increment_reflection_count()
                await self.db.commit()
                
        except Exception as e:
            logger.error(f"Error updating wisdom stats: {e}")
    
    async def _get_fallback_wisdom(self, user: User) -> Dict[str, Any]:
        """Get fallback wisdom if generation fails."""
        return {
            "id": "fallback",
            "date": date.today().isoformat(),
            "tradition": "universal",
            "type": "quote",
            "content": "The unexamined life is not worth living.",
            "source": "Socrates",
            "concepts": ["self-knowledge", "reflection", "wisdom"],
            "reflection_prompts": [
                "What does it mean to examine your life?",
                "How do you engage in self-reflection?",
                "What have you learned about yourself recently?"
            ],
            "estimated_time_minutes": 10,
            "difficulty_level": user.learning_level
        }
    
    async def get_user_reflection_history(
        self, 
        user_id: str, 
        limit: int = 30
    ) -> List[Dict[str, Any]]:
        """Get user's reflection history with analysis."""
        try:
            result = await self.db.execute(
                select(UserReflection)
                .where(UserReflection.user_id == user_id)
                .order_by(UserReflection.created_at.desc())
                .limit(limit)
            )
            reflections = result.scalars().all()
            
            history = []
            for reflection in reflections:
                history.append({
                    "id": str(reflection.id),
                    "date": reflection.created_at.date().isoformat(),
                    "depth_score": reflection.philosophical_depth_score,
                    "emotional_tone": reflection.emotional_tone,
                    "key_insights": reflection.key_insights or [],
                    "growth_indicators": reflection.growth_indicators or [],
                    "reflection_preview": reflection.reflection_text[:200] + "..." if len(reflection.reflection_text) > 200 else reflection.reflection_text
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting reflection history: {e}")
            return []