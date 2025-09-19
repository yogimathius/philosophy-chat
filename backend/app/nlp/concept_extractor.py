"""Philosophical concept extraction using NLP techniques."""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import spacy
from sentence_transformers import SentenceTransformer

from app.core.config import settings

logger = logging.getLogger(__name__)


class ConceptExtractor:
    """Extract philosophical concepts from text using multiple NLP techniques."""
    
    def __init__(self, nlp_model: spacy.Language):
        """Initialize concept extractor with spaCy model."""
        self.nlp = nlp_model
        self.sentence_model: Optional[SentenceTransformer] = None
        self.philosophical_terms: Set[str] = set()
        self.concept_embeddings: Dict[str, Any] = {}
        self.concept_definitions: Dict[str, str] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize concept extractor with philosophical knowledge base."""
        if self._initialized:
            return
        
        logger.info("Initializing concept extractor...")
        
        try:
            # Load sentence transformer for semantic similarity
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load philosophical terms and concepts
            await self._load_philosophical_knowledge()
            
            self._initialized = True
            logger.info("Concept extractor initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize concept extractor: {e}")
            raise
    
    async def _load_philosophical_knowledge(self) -> None:
        """Load philosophical terms and concepts from knowledge base."""
        # Core philosophical terms (expandable from database later)
        self.philosophical_terms = {
            # Ethics
            "virtue", "vice", "moral", "ethical", "justice", "fairness", "good", "evil",
            "right", "wrong", "duty", "responsibility", "consequentialism", "deontology",
            "utilitarianism", "categorical imperative", "virtue ethics", "moral relativism",
            
            # Metaphysics  
            "existence", "being", "reality", "substance", "essence", "identity", "causation",
            "determinism", "free will", "mind", "matter", "dualism", "materialism", "idealism",
            "phenomenology", "ontology", "metaphysics", "necessary", "contingent",
            
            # Epistemology
            "knowledge", "truth", "belief", "justified", "certainty", "doubt", "skepticism",
            "empiricism", "rationalism", "a priori", "a posteriori", "induction", "deduction",
            "fallibilism", "foundationalism", "coherentism", "relativism",
            
            # Philosophy of Mind
            "consciousness", "qualia", "intentionality", "mental", "physical", "reduction",
            "emergence", "functionalism", "behaviorism", "identity theory", "property dualism",
            
            # Existentialism
            "authenticity", "bad faith", "existential", "absurd", "freedom", "responsibility",
            "anxiety", "anguish", "thrownness", "facticity", "being-toward-death", "nausea",
            
            # Eastern Philosophy
            "dharma", "karma", "nirvana", "enlightenment", "suffering", "attachment",
            "impermanence", "interdependence", "mindfulness", "meditation", "wu wei", "tao",
            
            # Stoicism
            "stoicism", "stoic", "apatheia", "ataraxia", "preferred indifferent", "sage",
            "logos", "cosmic sympathy", "memento mori", "amor fati",
            
            # Political Philosophy
            "liberty", "equality", "democracy", "authority", "legitimacy", "social contract",
            "natural rights", "civil disobedience", "justice as fairness", "original position",
            
            # Aesthetics
            "beauty", "sublime", "aesthetic", "art", "taste", "judgment", "disinterested",
            
            # Logic
            "valid", "sound", "premise", "conclusion", "syllogism", "fallacy", "contradiction",
            "tautology", "modal logic", "possible worlds"
        }
        
        # Load concept definitions
        self.concept_definitions = {
            "virtue": "A character trait or disposition to act in ways that promote human flourishing",
            "justice": "The principle of giving each person their due, fairly distributing benefits and burdens",
            "consciousness": "The state of being aware and having subjective experiences",
            "free will": "The ability to make choices that are not entirely determined by prior causes",
            "authenticity": "Being true to one's own character, spirit, and values rather than conforming to external expectations",
            "absurd": "The conflict between human desire for meaning and the universe's apparent meaninglessness",
            "dharma": "Righteous living or moral law; one's duty in accordance with cosmic order",
            "stoicism": "A philosophy emphasizing virtue, wisdom, and acceptance of what cannot be changed",
            "empiricism": "The view that knowledge comes primarily from sensory experience",
            "categorical imperative": "Kant's principle that one should act only according to universalizable maxims"
        }
    
    async def extract_concepts(
        self, 
        text: str, 
        doc: spacy.Doc, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Extract philosophical concepts from text using multiple methods."""
        if not self._initialized:
            await self.initialize()
        
        concepts = []
        
        # Method 1: Direct term matching
        direct_matches = self._find_direct_matches(text)
        concepts.extend(direct_matches)
        
        # Method 2: Named entity recognition
        ner_concepts = self._extract_ner_concepts(doc)
        concepts.extend(ner_concepts)
        
        # Method 3: Semantic similarity matching
        semantic_concepts = await self._find_semantic_matches(text)
        concepts.extend(semantic_concepts)
        
        # Method 4: Pattern-based extraction
        pattern_concepts = self._extract_pattern_concepts(doc)
        concepts.extend(pattern_concepts)
        
        # Remove duplicates and rank by confidence
        unique_concepts = self._deduplicate_and_rank(concepts)
        
        # Filter by confidence threshold
        filtered_concepts = [
            concept for concept in unique_concepts 
            if concept["confidence"] >= settings.concept_extraction_threshold
        ]
        
        return {
            "concepts": filtered_concepts[:20],  # Limit to top 20
            "total_found": len(unique_concepts),
            "extraction_methods_used": ["direct", "ner", "semantic", "pattern"],
            "confidence_threshold": settings.concept_extraction_threshold
        }
    
    def _find_direct_matches(self, text: str) -> List[Dict[str, Any]]:
        """Find direct matches with known philosophical terms."""
        text_lower = text.lower()
        matches = []
        
        for term in self.philosophical_terms:
            if term in text_lower:
                # Calculate confidence based on exact vs partial match
                exact_matches = text_lower.count(term)
                confidence = min(1.0, exact_matches * 0.3 + 0.7)
                
                matches.append({
                    "name": term,
                    "confidence": confidence,
                    "method": "direct",
                    "occurrences": exact_matches,
                    "definition": self.concept_definitions.get(term, "")
                })
        
        return matches
    
    def _extract_ner_concepts(self, doc: spacy.Doc) -> List[Dict[str, Any]]:
        """Extract concepts using named entity recognition."""
        concepts = []
        
        # Look for person entities (philosophers)
        philosophers = {
            "aristotle", "plato", "socrates", "kant", "hume", "descartes", "nietzsche",
            "sartre", "heidegger", "wittgenstein", "russell", "aquinas", "spinoza",
            "buddha", "confucius", "lao tzu", "marcus aurelius", "epictetus", "seneca"
        }
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name_lower = ent.text.lower()
                if any(phil in name_lower for phil in philosophers):
                    concepts.append({
                        "name": f"{ent.text} (philosopher)",
                        "confidence": 0.8,
                        "method": "ner",
                        "entity_type": "philosopher",
                        "definition": f"Philosopher: {ent.text}"
                    })
        
        return concepts
    
    async def _find_semantic_matches(self, text: str) -> List[Dict[str, Any]]:
        """Find concepts using semantic similarity."""
        if not self.sentence_model:
            return []
        
        try:
            # Get text embedding
            text_embedding = self.sentence_model.encode([text])
            
            # Compare with concept embeddings (simplified for now)
            concepts = []
            
            # Key philosophical concepts for semantic matching
            key_concepts = [
                "moral responsibility", "personal identity", "meaning of life",
                "nature of reality", "source of knowledge", "mind-body problem",
                "existence of god", "political authority", "aesthetic experience"
            ]
            
            concept_embeddings = self.sentence_model.encode(key_concepts)
            
            # Calculate similarities
            from sklearn.metrics.pairwise import cosine_similarity
            similarities = cosine_similarity(text_embedding, concept_embeddings)[0]
            
            for i, (concept, similarity) in enumerate(zip(key_concepts, similarities)):
                if similarity > 0.3:  # Threshold for semantic similarity
                    concepts.append({
                        "name": concept,
                        "confidence": float(similarity),
                        "method": "semantic",
                        "similarity_score": float(similarity),
                        "definition": f"Philosophical concept: {concept}"
                    })
            
            return concepts
            
        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
            return []
    
    def _extract_pattern_concepts(self, doc: spacy.Doc) -> List[Dict[str, Any]]:
        """Extract concepts using linguistic patterns."""
        concepts = []
        
        # Pattern 1: "The concept of X"
        for token in doc:
            if (token.lemma_ == "concept" and 
                token.i + 2 < len(doc) and 
                doc[token.i + 1].text == "of"):
                
                concept_noun = doc[token.i + 2]
                if concept_noun.pos_ in ["NOUN", "PROPN"]:
                    concepts.append({
                        "name": concept_noun.text.lower(),
                        "confidence": 0.7,
                        "method": "pattern",
                        "pattern_type": "concept_of",
                        "definition": f"Philosophical concept related to {concept_noun.text}"
                    })
        
        # Pattern 2: "X is defined as Y"
        for sent in doc.sents:
            tokens = [t.text for t in sent]
            if "defined" in tokens and "as" in tokens:
                defined_idx = tokens.index("defined")
                if defined_idx > 0:
                    concept_word = tokens[defined_idx - 1]
                    concepts.append({
                        "name": concept_word.lower(),
                        "confidence": 0.6,
                        "method": "pattern",
                        "pattern_type": "definition",
                        "definition": f"Defined concept: {concept_word}"
                    })
        
        # Pattern 3: Abstract philosophical nouns
        abstract_indicators = {"nature", "essence", "meaning", "purpose", "truth", "reality"}
        for token in doc:
            if (token.lemma_ in abstract_indicators and 
                token.dep_ in ["nsubj", "dobj", "pobj"]):
                concepts.append({
                    "name": token.lemma_,
                    "confidence": 0.5,
                    "method": "pattern",
                    "pattern_type": "abstract_noun",
                    "definition": f"Abstract philosophical concept: {token.lemma_}"
                })
        
        return concepts
    
    def _deduplicate_and_rank(self, concepts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and rank concepts by confidence."""
        # Group by concept name
        concept_groups = {}
        for concept in concepts:
            name = concept["name"].lower().strip()
            if name not in concept_groups:
                concept_groups[name] = []
            concept_groups[name].append(concept)
        
        # For each group, take the highest confidence
        unique_concepts = []
        for name, group in concept_groups.items():
            best_concept = max(group, key=lambda x: x["confidence"])
            
            # Combine information from multiple methods
            methods_used = list(set(c["method"] for c in group))
            best_concept["methods_used"] = methods_used
            best_concept["total_detections"] = len(group)
            
            unique_concepts.append(best_concept)
        
        # Sort by confidence
        return sorted(unique_concepts, key=lambda x: x["confidence"], reverse=True)
    
    async def get_concept_definition(self, concept_name: str) -> Optional[str]:
        """Get definition for a specific concept."""
        concept_lower = concept_name.lower().strip()
        return self.concept_definitions.get(concept_lower)
    
    async def add_concept_definition(self, concept_name: str, definition: str) -> None:
        """Add a new concept definition to the knowledge base."""
        concept_lower = concept_name.lower().strip()
        self.concept_definitions[concept_lower] = definition
        self.philosophical_terms.add(concept_lower)
    
    def get_related_concepts(self, concept_name: str) -> List[str]:
        """Get concepts related to the given concept."""
        # Simple related concept mapping (can be enhanced with embeddings)
        relations = {
            "virtue": ["ethics", "moral", "good", "character", "excellence"],
            "justice": ["fairness", "rights", "law", "equality", "virtue"],
            "consciousness": ["mind", "awareness", "experience", "qualia", "subjectivity"],
            "free will": ["determinism", "responsibility", "choice", "causation", "agency"],
            "authenticity": ["bad faith", "existentialism", "self", "identity", "genuine"],
            "stoicism": ["virtue", "wisdom", "acceptance", "emotions", "reason"]
        }
        
        concept_lower = concept_name.lower().strip()
        return relations.get(concept_lower, [])