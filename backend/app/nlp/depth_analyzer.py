"""Philosophical depth analysis for text content."""

import asyncio
import logging
import re
from typing import Any, Dict, List, Optional

import spacy

from app.core.config import settings

logger = logging.getLogger(__name__)


class DepthAnalyzer:
    """Analyze philosophical depth and sophistication of text."""
    
    def __init__(self, nlp_model: spacy.Language):
        """Initialize depth analyzer with spaCy model."""
        self.nlp = nlp_model
        self.depth_indicators: Dict[str, List[str]] = {}
        self.sophistication_patterns: List[str] = []
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize depth analyzer with philosophical depth indicators."""
        if self._initialized:
            return
        
        logger.info("Initializing depth analyzer...")
        
        try:
            await self._load_depth_indicators()
            self._initialized = True
            logger.info("Depth analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize depth analyzer: {e}")
            raise
    
    async def _load_depth_indicators(self) -> None:
        """Load indicators of philosophical depth."""
        
        # Depth indicators by category
        self.depth_indicators = {
            "abstract_thinking": [
                "abstract", "conceptual", "theoretical", "metaphysical", "ontological",
                "epistemological", "phenomenological", "transcendental", "dialectical"
            ],
            
            "critical_analysis": [
                "however", "nevertheless", "on the contrary", "critique", "examine",
                "question", "challenge", "problematic", "paradox", "contradiction",
                "tension", "complexity", "nuance", "ambiguity"
            ],
            
            "philosophical_reasoning": [
                "therefore", "thus", "consequently", "follows that", "implies",
                "necessarily", "sufficient", "necessary condition", "entails",
                "presupposes", "assumes", "premise", "conclusion", "argument"
            ],
            
            "meta_reflection": [
                "reflect", "consider", "contemplate", "ponder", "introspect",
                "self-examination", "meta", "recursive", "self-referential",
                "awareness of", "consciousness of"
            ],
            
            "existential_inquiry": [
                "meaning", "purpose", "existence", "being", "authenticity",
                "freedom", "responsibility", "mortality", "absurd", "alienation",
                "anxiety", "despair", "hope", "transcendence"
            ],
            
            "ethical_sophistication": [
                "ought", "should", "moral", "ethical", "virtue", "vice", "duty",
                "obligation", "rights", "justice", "fairness", "good life",
                "human flourishing", "moral dilemma", "ethical framework"
            ],
            
            "historical_awareness": [
                "traditionally", "historically", "ancient", "medieval", "modern",
                "contemporary", "tradition", "heritage", "legacy", "influence",
                "development", "evolution", "progression"
            ],
            
            "comparative_thinking": [
                "compare", "contrast", "similar", "different", "whereas", "while",
                "on the other hand", "alternatively", "in contrast to",
                "distinguish", "differentiate", "analogous", "parallel"
            ]
        }
        
        # Sophistication patterns (regex patterns for complex constructions)
        self.sophistication_patterns = [
            r"not only.*but also",  # Complex conjunctions
            r"insofar as",  # Conditional reasoning
            r"to the extent that",  # Qualified statements
            r"inasmuch as",  # Causal reasoning
            r"the fact that.*suggests",  # Evidence-based reasoning
            r"it could be argued that",  # Tentative reasoning
            r"one might object that",  # Anticipating counterarguments
            r"this raises the question",  # Question generation
            r"the implications of.*are",  # Consequence analysis
            r"the paradox.*lies in",  # Paradox identification
        ]
    
    async def analyze_depth(
        self, 
        text: str, 
        doc: spacy.Doc, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze the philosophical depth of text."""
        if not self._initialized:
            await self.initialize()
        
        # Calculate various depth metrics
        indicator_scores = self._analyze_depth_indicators(text)
        reasoning_complexity = self._analyze_reasoning_complexity(doc)
        question_sophistication = self._analyze_questions(text)
        conceptual_density = self._analyze_conceptual_density(doc)
        synthesis_level = self._analyze_synthesis(text, doc)
        
        # Calculate overall depth score (1-10)
        depth_score = self._calculate_overall_depth(
            indicator_scores, reasoning_complexity, question_sophistication,
            conceptual_density, synthesis_level
        )
        
        # Identify specific depth markers
        depth_markers = self._identify_depth_markers(text, doc)
        
        # Suggest improvements for shallow content
        improvement_suggestions = self._suggest_improvements(depth_score, indicator_scores)
        
        return {
            "depth_score": depth_score,
            "indicator_scores": indicator_scores,
            "reasoning_complexity": reasoning_complexity,
            "question_sophistication": question_sophistication,
            "conceptual_density": conceptual_density,
            "synthesis_level": synthesis_level,
            "depth_markers": depth_markers,
            "improvement_suggestions": improvement_suggestions,
            "depth_category": self._categorize_depth(depth_score)
        }
    
    def _analyze_depth_indicators(self, text: str) -> Dict[str, float]:
        """Analyze presence of depth indicators by category."""
        text_lower = text.lower()
        word_count = len(text.split())
        
        scores = {}
        for category, indicators in self.depth_indicators.items():
            # Count occurrences of indicators
            total_occurrences = sum(text_lower.count(indicator) for indicator in indicators)
            
            # Calculate density (occurrences per 100 words)
            density = (total_occurrences / word_count) * 100 if word_count > 0 else 0
            
            # Convert to 0-10 scale
            scores[category] = min(10, density * 2)
        
        return scores
    
    def _analyze_reasoning_complexity(self, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze complexity of reasoning structures."""
        sentences = list(doc.sents)
        
        # Count conditional statements
        conditionals = 0
        for sent in sentences:
            sent_text = sent.text.lower()
            if any(cond in sent_text for cond in ["if", "when", "unless", "provided", "given"]):
                conditionals += 1
        
        # Count causal relationships
        causal_markers = ["because", "since", "due to", "results in", "leads to", "causes"]
        causal_statements = 0
        for sent in sentences:
            sent_text = sent.text.lower()
            if any(marker in sent_text for marker in causal_markers):
                causal_statements += 1
        
        # Count complex sentence structures
        complex_sentences = 0
        for sent in sentences:
            # Count subordinate clauses (simplified)
            subordinating_conjunctions = ["although", "while", "whereas", "since", "because"]
            if any(conj in sent.text.lower() for conj in subordinating_conjunctions):
                complex_sentences += 1
        
        # Calculate reasoning complexity score
        total_sentences = len(sentences)
        if total_sentences == 0:
            complexity_score = 0
        else:
            conditional_ratio = conditionals / total_sentences
            causal_ratio = causal_statements / total_sentences
            complex_ratio = complex_sentences / total_sentences
            
            complexity_score = min(10, (conditional_ratio + causal_ratio + complex_ratio) * 10)
        
        return {
            "complexity_score": round(complexity_score, 1),
            "conditional_statements": conditionals,
            "causal_statements": causal_statements,
            "complex_sentences": complex_sentences,
            "total_sentences": total_sentences
        }
    
    def _analyze_questions(self, text: str) -> Dict[str, Any]:
        """Analyze sophistication of questions in the text."""
        # Find all questions
        questions = re.findall(r'[^.!?]*\?', text)
        
        if not questions:
            return {"sophistication_score": 0, "question_types": [], "question_count": 0}
        
        # Analyze question types
        question_types = []
        sophistication_scores = []
        
        for question in questions:
            q_lower = question.lower().strip()
            
            # Categorize questions by sophistication
            if any(word in q_lower for word in ["what", "who", "where", "when"]):
                question_types.append("factual")
                sophistication_scores.append(2)
            
            elif any(word in q_lower for word in ["how", "why"]):
                question_types.append("explanatory")
                sophistication_scores.append(5)
            
            elif any(phrase in q_lower for phrase in ["what if", "suppose", "imagine"]):
                question_types.append("hypothetical")
                sophistication_scores.append(7)
            
            elif any(phrase in q_lower for phrase in ["should we", "ought", "is it right"]):
                question_types.append("normative")
                sophistication_scores.append(8)
            
            elif any(phrase in q_lower for phrase in ["what does it mean", "how can we understand"]):
                question_types.append("interpretive")
                sophistication_scores.append(9)
            
            elif any(phrase in q_lower for phrase in ["can we know", "is it possible", "what are the limits"]):
                question_types.append("epistemological")
                sophistication_scores.append(10)
            
            else:
                question_types.append("general")
                sophistication_scores.append(3)
        
        # Calculate average sophistication
        avg_sophistication = sum(sophistication_scores) / len(sophistication_scores) if sophistication_scores else 0
        
        return {
            "sophistication_score": round(avg_sophistication, 1),
            "question_types": list(set(question_types)),
            "question_count": len(questions),
            "questions_analyzed": questions[:3]  # Show first 3 questions
        }
    
    def _analyze_conceptual_density(self, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze density of abstract/conceptual language."""
        words = [token for token in doc if token.is_alpha and not token.is_stop]
        
        if not words:
            return {"density_score": 0, "abstract_words": []}
        
        # Abstract/conceptual words
        abstract_words = []
        abstract_indicators = {
            "concept", "idea", "notion", "principle", "theory", "framework",
            "essence", "nature", "reality", "truth", "meaning", "purpose",
            "significance", "value", "worth", "quality", "property", "attribute"
        }
        
        for word in words:
            lemma_lower = word.lemma_.lower()
            if lemma_lower in abstract_indicators:
                abstract_words.append(word.text)
        
        # Calculate density
        density = len(abstract_words) / len(words) if words else 0
        density_score = min(10, density * 20)  # Scale to 0-10
        
        return {
            "density_score": round(density_score, 1),
            "abstract_words": list(set(abstract_words)),
            "abstract_word_count": len(abstract_words),
            "total_words": len(words),
            "density_ratio": round(density, 3)
        }
    
    def _analyze_synthesis(self, text: str, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze level of synthesis and integration in the text."""
        text_lower = text.lower()
        
        # Synthesis indicators
        synthesis_markers = [
            "connects to", "relates to", "links with", "builds on", "extends",
            "integrates", "synthesizes", "combines", "unifies", "bridges",
            "draws together", "brings together", "weaves", "interconnects"
        ]
        
        # Cross-reference indicators
        reference_markers = [
            "as mentioned", "as discussed", "earlier", "previously", "above",
            "building on", "following from", "in light of", "considering"
        ]
        
        # Count synthesis and reference markers
        synthesis_count = sum(text_lower.count(marker) for marker in synthesis_markers)
        reference_count = sum(text_lower.count(marker) for marker in reference_markers)
        
        # Calculate synthesis score
        word_count = len(text.split())
        synthesis_density = (synthesis_count + reference_count) / (word_count / 100) if word_count > 0 else 0
        synthesis_score = min(10, synthesis_density * 2)
        
        return {
            "synthesis_score": round(synthesis_score, 1),
            "synthesis_markers": synthesis_count,
            "reference_markers": reference_count,
            "integration_level": "high" if synthesis_score > 7 else "medium" if synthesis_score > 4 else "low"
        }
    
    def _calculate_overall_depth(
        self, 
        indicator_scores: Dict[str, float],
        reasoning: Dict[str, Any],
        questions: Dict[str, Any],
        concepts: Dict[str, Any],
        synthesis: Dict[str, Any]
    ) -> float:
        """Calculate overall philosophical depth score."""
        
        # Weight different components
        weights = {
            "indicators": 0.3,
            "reasoning": 0.25,
            "questions": 0.2,
            "concepts": 0.15,
            "synthesis": 0.1
        }
        
        # Calculate weighted average of indicator scores
        avg_indicators = sum(indicator_scores.values()) / len(indicator_scores) if indicator_scores else 0
        
        # Get component scores
        reasoning_score = reasoning.get("complexity_score", 0)
        question_score = questions.get("sophistication_score", 0)
        concept_score = concepts.get("density_score", 0)
        synthesis_score = synthesis.get("synthesis_score", 0)
        
        # Calculate weighted overall score
        overall_score = (
            avg_indicators * weights["indicators"] +
            reasoning_score * weights["reasoning"] +
            question_score * weights["questions"] +
            concept_score * weights["concepts"] +
            synthesis_score * weights["synthesis"]
        )
        
        return round(min(10, max(1, overall_score)), 1)
    
    def _identify_depth_markers(self, text: str, doc: spacy.Doc) -> List[str]:
        """Identify specific markers of philosophical depth."""
        markers = []
        
        # Check for sophistication patterns
        for pattern in self.sophistication_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                markers.append(f"Complex construction: {pattern}")
        
        # Check for philosophical terminology density
        philosophical_terms = ["metaphysical", "epistemological", "ontological", "phenomenological"]
        found_terms = [term for term in philosophical_terms if term in text.lower()]
        if found_terms:
            markers.append(f"Philosophical terminology: {', '.join(found_terms)}")
        
        # Check for argumentation structure
        if "premise" in text.lower() and "conclusion" in text.lower():
            markers.append("Formal argumentation structure")
        
        # Check for counter-argument consideration
        counter_phrases = ["however", "on the other hand", "one might object", "critics argue"]
        if any(phrase in text.lower() for phrase in counter_phrases):
            markers.append("Counter-argument consideration")
        
        return markers
    
    def _suggest_improvements(self, depth_score: float, indicator_scores: Dict[str, float]) -> List[str]:
        """Suggest improvements for shallow philosophical content."""
        suggestions = []
        
        if depth_score < 6:
            suggestions.append("Consider adding more abstract reasoning and conceptual analysis")
            
            # Specific suggestions based on low indicator scores
            if indicator_scores.get("critical_analysis", 0) < 5:
                suggestions.append("Include more critical examination and questioning of assumptions")
            
            if indicator_scores.get("philosophical_reasoning", 0) < 5:
                suggestions.append("Strengthen logical reasoning with premises and conclusions")
            
            if indicator_scores.get("existential_inquiry", 0) < 5:
                suggestions.append("Explore deeper questions about meaning, purpose, and existence")
            
            if indicator_scores.get("comparative_thinking", 0) < 5:
                suggestions.append("Compare and contrast different philosophical perspectives")
            
            if depth_score < 4:
                suggestions.append("Consider reading primary philosophical texts to deepen understanding")
        
        return suggestions
    
    def _categorize_depth(self, depth_score: float) -> str:
        """Categorize depth level based on score."""
        if depth_score >= 8.5:
            return "profound"
        elif depth_score >= 7:
            return "deep"
        elif depth_score >= 5.5:
            return "moderate"
        elif depth_score >= 4:
            return "surface"
        else:
            return "shallow"