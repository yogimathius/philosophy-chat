"""Main NLP pipeline for philosophical text analysis."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import spacy
from transformers import pipeline

from app.core.config import settings
from .concept_extractor import ConceptExtractor
from .depth_analyzer import DepthAnalyzer
from .emotion_analyzer import EmotionAnalyzer
from .semantic_analyzer import SemanticAnalyzer

logger = logging.getLogger(__name__)


class NLPPipeline:
    """Advanced NLP pipeline for comprehensive philosophical text analysis."""
    
    def __init__(self):
        """Initialize the NLP pipeline with all components."""
        self.nlp: Optional[spacy.Language] = None
        self.concept_extractor: Optional[ConceptExtractor] = None
        self.depth_analyzer: Optional[DepthAnalyzer] = None
        self.emotion_analyzer: Optional[EmotionAnalyzer] = None
        self.semantic_analyzer: Optional[SemanticAnalyzer] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize all NLP components asynchronously."""
        if self._initialized:
            return
        
        logger.info("Initializing NLP pipeline...")
        
        try:
            # Load spaCy model
            self.nlp = spacy.load(settings.spacy_model)
            logger.info(f"Loaded spaCy model: {settings.spacy_model}")
            
            # Initialize components
            self.concept_extractor = ConceptExtractor(self.nlp)
            self.depth_analyzer = DepthAnalyzer(self.nlp)
            self.emotion_analyzer = EmotionAnalyzer()
            self.semantic_analyzer = SemanticAnalyzer(self.nlp)
            
            # Initialize all components
            await asyncio.gather(
                self.concept_extractor.initialize(),
                self.depth_analyzer.initialize(),
                self.emotion_analyzer.initialize(),
                self.semantic_analyzer.initialize(),
            )
            
            self._initialized = True
            logger.info("NLP pipeline initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize NLP pipeline: {e}")
            raise
    
    async def analyze_text(
        self, 
        text: str, 
        context: Optional[Dict[str, Any]] = None,
        analysis_types: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of philosophical text.
        
        Args:
            text: Text to analyze
            context: Optional context information
            analysis_types: List of analysis types to perform (default: all)
            
        Returns:
            Dictionary containing all analysis results
        """
        if not self._initialized:
            await self.initialize()
        
        if not text or not text.strip():
            return {"error": "Empty text provided"}
        
        # Default to all analysis types
        if analysis_types is None:
            analysis_types = [
                "concepts", "depth", "emotions", "semantics", 
                "complexity", "coherence", "themes"
            ]
        
        logger.debug(f"Analyzing text with types: {analysis_types}")
        
        try:
            # Process text through spaCy first
            doc = self.nlp(text)
            
            # Prepare analysis tasks
            tasks = []
            
            if "concepts" in analysis_types:
                tasks.append(self._analyze_concepts(text, doc, context))
            
            if "depth" in analysis_types:
                tasks.append(self._analyze_depth(text, doc, context))
            
            if "emotions" in analysis_types:
                tasks.append(self._analyze_emotions(text, context))
            
            if "semantics" in analysis_types:
                tasks.append(self._analyze_semantics(text, doc, context))
            
            if "complexity" in analysis_types:
                tasks.append(self._analyze_complexity(text, doc))
            
            if "coherence" in analysis_types:
                tasks.append(self._analyze_coherence(text, doc))
            
            if "themes" in analysis_types:
                tasks.append(self._analyze_themes(text, doc, context))
            
            # Run all analyses in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            analysis_result = {
                "text": text,
                "word_count": len(text.split()),
                "sentence_count": len(list(doc.sents)),
                "timestamp": asyncio.get_event_loop().time(),
                "analysis_types": analysis_types,
            }
            
            # Add individual analysis results
            for i, task_type in enumerate([t for t in analysis_types if t in [
                "concepts", "depth", "emotions", "semantics", 
                "complexity", "coherence", "themes"
            ]]):
                if i < len(results):
                    result = results[i]
                    if isinstance(result, Exception):
                        logger.error(f"Error in {task_type} analysis: {result}")
                        analysis_result[task_type] = {"error": str(result)}
                    else:
                        analysis_result[task_type] = result
            
            # Add overall scores
            analysis_result["overall_scores"] = self._calculate_overall_scores(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in text analysis: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    async def _analyze_concepts(
        self, text: str, doc: spacy.Doc, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract philosophical concepts from text."""
        return await self.concept_extractor.extract_concepts(text, doc, context)
    
    async def _analyze_depth(
        self, text: str, doc: spacy.Doc, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze philosophical depth of text."""
        return await self.depth_analyzer.analyze_depth(text, doc, context)
    
    async def _analyze_emotions(
        self, text: str, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze emotional tone of text."""
        return await self.emotion_analyzer.analyze_emotions(text, context)
    
    async def _analyze_semantics(
        self, text: str, doc: spacy.Doc, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Perform semantic analysis of text."""
        return await self.semantic_analyzer.analyze_semantics(text, doc, context)
    
    async def _analyze_complexity(self, text: str, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze text complexity."""
        # Basic complexity metrics
        sentences = list(doc.sents)
        words = [token for token in doc if not token.is_space and not token.is_punct]
        
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        avg_word_length = sum(len(token.text) for token in words) / len(words) if words else 0
        
        # Count unique words
        unique_words = set(token.lemma_.lower() for token in words if token.is_alpha)
        lexical_diversity = len(unique_words) / len(words) if words else 0
        
        # Philosophical vocabulary density
        philosophical_words = [
            token for token in words 
            if token.lemma_.lower() in self.concept_extractor.philosophical_terms
        ]
        phil_density = len(philosophical_words) / len(words) if words else 0
        
        # Overall complexity score (1-10)
        complexity_score = min(10, max(1, 
            (avg_sentence_length / 5) * 0.3 +
            (avg_word_length / 2) * 0.2 +
            (lexical_diversity * 10) * 0.3 +
            (phil_density * 10) * 0.2
        ))
        
        return {
            "complexity_score": round(complexity_score, 1),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "avg_word_length": round(avg_word_length, 1),
            "lexical_diversity": round(lexical_diversity, 3),
            "philosophical_density": round(phil_density, 3),
            "unique_word_count": len(unique_words),
            "total_words": len(words),
            "sentence_count": len(sentences)
        }
    
    async def _analyze_coherence(self, text: str, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze text coherence and flow."""
        sentences = list(doc.sents)
        
        if len(sentences) < 2:
            return {"coherence_score": 10.0, "flow_indicators": []}
        
        # Simple coherence indicators
        flow_indicators = []
        
        # Check for transition words
        transition_words = {
            "however", "therefore", "thus", "furthermore", "moreover", 
            "consequently", "nevertheless", "indeed", "similarly", "likewise"
        }
        
        transition_count = sum(
            1 for token in doc 
            if token.lemma_.lower() in transition_words
        )
        
        if transition_count > 0:
            flow_indicators.append("Uses transition words")
        
        # Check for pronoun reference (simple coherence indicator)
        pronouns = [token for token in doc if token.pos_ == "PRON"]
        if len(pronouns) > len(sentences):
            flow_indicators.append("Good pronoun usage for coherence")
        
        # Basic coherence score
        coherence_score = min(10, max(1, 
            7 + (transition_count * 0.5) - (abs(len(sentences) - 5) * 0.1)
        ))
        
        return {
            "coherence_score": round(coherence_score, 1),
            "flow_indicators": flow_indicators,
            "transition_word_count": transition_count,
            "pronoun_count": len(pronouns)
        }
    
    async def _analyze_themes(
        self, text: str, doc: spacy.Doc, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Identify philosophical themes in text."""
        themes = {}
        
        # Define theme keywords
        theme_keywords = {
            "ethics": ["moral", "ethical", "right", "wrong", "virtue", "good", "evil", "justice"],
            "metaphysics": ["reality", "existence", "being", "nature", "substance", "cause"],
            "epistemology": ["knowledge", "truth", "belief", "certainty", "doubt", "evidence"],
            "consciousness": ["mind", "consciousness", "awareness", "experience", "perception"],
            "meaning": ["meaning", "purpose", "significance", "value", "worth"],
            "freedom": ["freedom", "liberty", "choice", "determinism", "responsibility"],
            "death": ["death", "mortality", "immortality", "dying", "afterlife"],
            "time": ["time", "temporal", "eternity", "moment", "duration", "past", "future"]
        }
        
        # Count theme occurrences
        text_lower = text.lower()
        for theme, keywords in theme_keywords.items():
            count = sum(text_lower.count(keyword) for keyword in keywords)
            if count > 0:
                themes[theme] = {
                    "count": count,
                    "relevance": min(1.0, count / (len(text.split()) / 100))
                }
        
        # Sort themes by relevance
        sorted_themes = sorted(themes.items(), key=lambda x: x[1]["relevance"], reverse=True)
        
        return {
            "themes": dict(sorted_themes),
            "primary_theme": sorted_themes[0][0] if sorted_themes else None,
            "theme_diversity": len(themes)
        }
    
    def _calculate_overall_scores(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall analysis scores."""
        scores = {}
        
        # Extract individual scores
        depth_score = analysis.get("depth", {}).get("depth_score", 5)
        complexity_score = analysis.get("complexity", {}).get("complexity_score", 5)
        coherence_score = analysis.get("coherence", {}).get("coherence_score", 5)
        concept_count = len(analysis.get("concepts", {}).get("concepts", []))
        
        # Overall philosophical quality (1-10)
        quality_score = (depth_score * 0.4 + complexity_score * 0.3 + coherence_score * 0.3)
        
        # Philosophical richness based on concept density
        richness_score = min(10, max(1, concept_count * 2))
        
        scores["quality_score"] = round(quality_score, 1)
        scores["richness_score"] = round(richness_score, 1)
        scores["overall_score"] = round((quality_score + richness_score) / 2, 1)
        
        return scores
    
    async def analyze_conversation_context(
        self, messages: List[Dict[str, str]], max_context: int = 10
    ) -> Dict[str, Any]:
        """Analyze conversation context for better AI responses."""
        if not self._initialized:
            await self.initialize()
        
        # Take recent messages
        recent_messages = messages[-max_context:] if messages else []
        
        if not recent_messages:
            return {"concepts": [], "themes": [], "emotional_journey": []}
        
        # Combine all text for analysis
        combined_text = " ".join([msg.get("content", "") for msg in recent_messages])
        
        # Analyze the combined context
        context_analysis = await self.analyze_text(
            combined_text, 
            analysis_types=["concepts", "emotions", "themes"]
        )
        
        # Track emotional journey
        emotional_journey = []
        for msg in recent_messages:
            msg_analysis = await self.analyze_text(
                msg.get("content", ""), 
                analysis_types=["emotions"]
            )
            emotional_journey.append({
                "sender": msg.get("sender", "unknown"),
                "emotion": msg_analysis.get("emotions", {}).get("primary_emotion", "neutral"),
                "confidence": msg_analysis.get("emotions", {}).get("confidence", 0.5)
            })
        
        return {
            "context_concepts": context_analysis.get("concepts", {}).get("concepts", []),
            "context_themes": context_analysis.get("themes", {}).get("themes", {}),
            "emotional_journey": emotional_journey,
            "conversation_depth": context_analysis.get("depth", {}).get("depth_score", 5),
            "message_count": len(recent_messages)
        }


# Global pipeline instance
nlp_pipeline = NLPPipeline()