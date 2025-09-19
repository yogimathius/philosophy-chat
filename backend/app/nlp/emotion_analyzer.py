"""Emotional tone analysis for philosophical text with context awareness."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from transformers import pipeline

logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """Analyze emotional tone and philosophical mood in text."""
    
    def __init__(self):
        """Initialize emotion analyzer."""
        self.emotion_pipeline = None
        self.sentiment_pipeline = None
        self.philosophical_emotions: Dict[str, List[str]] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize emotion analysis models."""
        if self._initialized:
            return
        
        logger.info("Initializing emotion analyzer...")
        
        try:
            # Load emotion classification model
            self.emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
            
            # Load sentiment analysis model
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            
            # Define philosophical emotion categories
            await self._load_philosophical_emotions()
            
            self._initialized = True
            logger.info("Emotion analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize emotion analyzer: {e}")
            raise
    
    async def _load_philosophical_emotions(self) -> None:
        """Load philosophical emotion categories and associations."""
        self.philosophical_emotions = {
            "wonder": [
                "curious", "amazed", "intrigued", "fascinated", "awed", 
                "puzzled", "mystified", "enchanted"
            ],
            
            "contemplation": [
                "reflective", "thoughtful", "meditative", "pensive", 
                "introspective", "absorbed", "focused", "concentrated"
            ],
            
            "existential_anxiety": [
                "anxious", "uncertain", "troubled", "unsettled", "restless",
                "questioning", "doubtful", "searching", "yearning"
            ],
            
            "intellectual_excitement": [
                "excited", "enthusiastic", "energized", "inspired", 
                "motivated", "passionate", "engaged", "stimulated"
            ],
            
            "moral_concern": [
                "concerned", "worried", "troubled", "distressed", 
                "compassionate", "empathetic", "caring", "responsible"
            ],
            
            "philosophical_satisfaction": [
                "satisfied", "fulfilled", "content", "peaceful", "resolved",
                "clear", "understanding", "enlightened", "wise"
            ],
            
            "critical_doubt": [
                "skeptical", "doubtful", "questioning", "critical", 
                "suspicious", "hesitant", "uncertain", "cautious"
            ],
            
            "transcendent_joy": [
                "joyful", "blissful", "ecstatic", "euphoric", "elevated",
                "transcendent", "spiritual", "connected", "unified"
            ],
            
            "melancholic_wisdom": [
                "sad", "melancholic", "wistful", "nostalgic", "bittersweet",
                "wise", "mature", "accepting", "resigned"
            ]
        }
    
    async def analyze_emotions(
        self, 
        text: str, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze emotions and philosophical mood in text."""
        if not self._initialized:
            await self.initialize()
        
        if not text or not text.strip():
            return {"error": "Empty text provided"}
        
        try:
            # Get basic emotions
            basic_emotions = await self._analyze_basic_emotions(text)
            
            # Get sentiment
            sentiment = await self._analyze_sentiment(text)
            
            # Identify philosophical emotions
            philosophical_mood = self._identify_philosophical_mood(text, basic_emotions)
            
            # Analyze emotional journey (if context provided)
            emotional_journey = self._analyze_emotional_journey(text, context)
            
            # Get emotional depth and complexity
            emotional_complexity = self._analyze_emotional_complexity(text, basic_emotions)
            
            # Determine primary emotion and confidence
            primary_emotion, confidence = self._determine_primary_emotion(basic_emotions, philosophical_mood)
            
            return {
                "primary_emotion": primary_emotion,
                "confidence": confidence,
                "basic_emotions": basic_emotions,
                "sentiment": sentiment,
                "philosophical_mood": philosophical_mood,
                "emotional_journey": emotional_journey,
                "emotional_complexity": emotional_complexity,
                "emotion_category": self._categorize_emotion(primary_emotion),
                "philosophical_relevance": self._assess_philosophical_relevance(philosophical_mood)
            }
            
        except Exception as e:
            logger.error(f"Error in emotion analysis: {e}")
            return {"error": f"Emotion analysis failed: {str(e)}"}
    
    async def _analyze_basic_emotions(self, text: str) -> Dict[str, float]:
        """Analyze basic emotions using transformer model."""
        try:
            # Get emotion predictions
            emotion_results = self.emotion_pipeline(text)
            
            # Convert to dictionary with scores
            emotions = {}
            for result in emotion_results[0]:  # First (and only) text
                emotions[result["label"]] = result["score"]
            
            return emotions
            
        except Exception as e:
            logger.error(f"Error in basic emotion analysis: {e}")
            return {"neutral": 0.5}
    
    async def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze sentiment polarity."""
        try:
            # Get sentiment predictions
            sentiment_results = self.sentiment_pipeline(text)
            
            # Convert to dictionary
            sentiment = {}
            for result in sentiment_results[0]:
                # Map labels to standard names
                label = result["label"].lower()
                if "pos" in label:
                    sentiment["positive"] = result["score"]
                elif "neg" in label:
                    sentiment["negative"] = result["score"]
                else:
                    sentiment["neutral"] = result["score"]
            
            return sentiment
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {"neutral": 0.5, "positive": 0.25, "negative": 0.25}
    
    def _identify_philosophical_mood(
        self, 
        text: str, 
        basic_emotions: Dict[str, float]
    ) -> Dict[str, Any]:
        """Identify philosophical mood based on text and emotions."""
        text_lower = text.lower()
        philosophical_moods = {}
        
        # Check for philosophical emotion indicators in text
        for mood, indicators in self.philosophical_emotions.items():
            # Count indicator words in text
            indicator_count = sum(
                text_lower.count(indicator) for indicator in indicators
            )
            
            # Weight by text length
            word_count = len(text.split())
            indicator_density = indicator_count / (word_count / 100) if word_count > 0 else 0
            
            # Combine with basic emotion scores
            relevant_basic_emotions = self._map_to_basic_emotions(mood)
            emotion_alignment = sum(
                basic_emotions.get(emotion, 0) for emotion in relevant_basic_emotions
            ) / len(relevant_basic_emotions) if relevant_basic_emotions else 0
            
            # Calculate overall mood score
            mood_score = (indicator_density * 0.4 + emotion_alignment * 0.6)
            
            if mood_score > 0.1:  # Threshold for relevance
                philosophical_moods[mood] = {
                    "score": round(mood_score, 3),
                    "indicator_count": indicator_count,
                    "emotion_alignment": round(emotion_alignment, 3)
                }
        
        # Sort by score
        sorted_moods = dict(sorted(
            philosophical_moods.items(), 
            key=lambda x: x[1]["score"], 
            reverse=True
        ))
        
        return {
            "moods": sorted_moods,
            "primary_mood": list(sorted_moods.keys())[0] if sorted_moods else "neutral",
            "mood_diversity": len(sorted_moods)
        }
    
    def _map_to_basic_emotions(self, philosophical_mood: str) -> List[str]:
        """Map philosophical moods to basic emotion categories."""
        mapping = {
            "wonder": ["surprise", "joy"],
            "contemplation": ["neutral", "calm"],
            "existential_anxiety": ["fear", "sadness", "surprise"],
            "intellectual_excitement": ["joy", "surprise"],
            "moral_concern": ["sadness", "fear", "anger"],
            "philosophical_satisfaction": ["joy", "calm"],
            "critical_doubt": ["fear", "neutral"],
            "transcendent_joy": ["joy", "surprise"],
            "melancholic_wisdom": ["sadness", "neutral"]
        }
        return mapping.get(philosophical_mood, ["neutral"])
    
    def _analyze_emotional_journey(
        self, 
        text: str, 
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze emotional progression through the text."""
        # Split text into segments for journey analysis
        sentences = text.split(". ")
        if len(sentences) < 3:
            return {"journey_detected": False}
        
        # Analyze emotional progression (simplified)
        journey_markers = {
            "progression": ["then", "next", "after", "subsequently", "finally"],
            "contrast": ["but", "however", "yet", "still", "nonetheless"],
            "resolution": ["therefore", "thus", "ultimately", "in conclusion"]
        }
        
        journey_elements = []
        for marker_type, markers in journey_markers.items():
            for marker in markers:
                if marker in text.lower():
                    journey_elements.append(marker_type)
        
        return {
            "journey_detected": len(journey_elements) > 0,
            "journey_elements": list(set(journey_elements)),
            "text_segments": len(sentences),
            "progression_indicators": journey_elements.count("progression"),
            "emotional_shifts": journey_elements.count("contrast")
        }
    
    def _analyze_emotional_complexity(
        self, 
        text: str, 
        basic_emotions: Dict[str, float]
    ) -> Dict[str, Any]:
        """Analyze complexity and nuance of emotional expression."""
        # Count number of emotions above threshold
        significant_emotions = [
            emotion for emotion, score in basic_emotions.items() 
            if score > 0.2
        ]
        
        # Analyze emotional vocabulary diversity
        emotional_words = [
            "feel", "feeling", "felt", "emotion", "emotional", "mood",
            "heart", "soul", "spirit", "passion", "love", "hate", "fear",
            "joy", "sadness", "anger", "surprise", "disgust", "trust"
        ]
        
        text_lower = text.lower()
        emotional_vocabulary_count = sum(
            text_lower.count(word) for word in emotional_words
        )
        
        # Check for emotional nuance indicators
        nuance_indicators = [
            "mixed feelings", "conflicted", "complex", "nuanced", 
            "ambivalent", "bittersweet", "paradoxical"
        ]
        
        nuance_count = sum(text_lower.count(indicator) for indicator in nuance_indicators)
        
        # Calculate complexity score
        word_count = len(text.split())
        complexity_score = min(10, 
            len(significant_emotions) * 1.5 +
            (emotional_vocabulary_count / (word_count / 100)) +
            nuance_count * 2
        )
        
        return {
            "complexity_score": round(complexity_score, 1),
            "significant_emotions": significant_emotions,
            "emotional_vocabulary_density": round(emotional_vocabulary_count / (word_count / 100), 2) if word_count > 0 else 0,
            "nuance_indicators": nuance_count,
            "emotional_range": len(significant_emotions)
        }
    
    def _determine_primary_emotion(
        self, 
        basic_emotions: Dict[str, float], 
        philosophical_mood: Dict[str, Any]
    ) -> tuple[str, float]:
        """Determine primary emotion and confidence level."""
        # Get highest scoring basic emotion
        if basic_emotions:
            primary_basic = max(basic_emotions.items(), key=lambda x: x[1])
        else:
            primary_basic = ("neutral", 0.5)
        
        # Get primary philosophical mood
        moods = philosophical_mood.get("moods", {})
        if moods:
            primary_mood = list(moods.keys())[0]
            mood_score = moods[primary_mood]["score"]
            
            # If philosophical mood is strong, use it as primary
            if mood_score > primary_basic[1] * 0.8:
                return primary_mood, mood_score
        
        return primary_basic[0], primary_basic[1]
    
    def _categorize_emotion(self, emotion: str) -> str:
        """Categorize emotion into broader philosophical categories."""
        categories = {
            "cognitive": ["wonder", "contemplation", "critical_doubt", "intellectual_excitement"],
            "existential": ["existential_anxiety", "melancholic_wisdom", "transcendent_joy"],
            "moral": ["moral_concern", "philosophical_satisfaction"],
            "basic": ["joy", "sadness", "anger", "fear", "surprise", "disgust", "trust"]
        }
        
        for category, emotions in categories.items():
            if emotion in emotions:
                return category
        
        return "neutral"
    
    def _assess_philosophical_relevance(self, philosophical_mood: Dict[str, Any]) -> Dict[str, Any]:
        """Assess how philosophically relevant the emotional content is."""
        moods = philosophical_mood.get("moods", {})
        
        if not moods:
            return {"relevance": "low", "score": 0.1}
        
        # Calculate overall philosophical relevance
        total_score = sum(mood_data["score"] for mood_data in moods.values())
        mood_count = len(moods)
        
        avg_relevance = total_score / mood_count if mood_count > 0 else 0
        
        # Categorize relevance
        if avg_relevance > 0.7:
            relevance = "very_high"
        elif avg_relevance > 0.5:
            relevance = "high"
        elif avg_relevance > 0.3:
            relevance = "moderate"
        elif avg_relevance > 0.1:
            relevance = "low"
        else:
            relevance = "minimal"
        
        return {
            "relevance": relevance,
            "score": round(avg_relevance, 3),
            "philosophical_mood_count": mood_count,
            "strongest_philosophical_emotion": list(moods.keys())[0] if moods else None
        }