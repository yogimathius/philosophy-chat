"""Semantic analysis for philosophical text understanding."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple

import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class SemanticAnalyzer:
    """Analyze semantic meaning and relationships in philosophical text."""
    
    def __init__(self, nlp_model: spacy.Language):
        """Initialize semantic analyzer with spaCy model."""
        self.nlp = nlp_model
        self.sentence_model: Optional[SentenceTransformer] = None
        self.philosophical_domains: Dict[str, List[str]] = {}
        self.domain_embeddings: Dict[str, np.ndarray] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize semantic analyzer with models and knowledge base."""
        if self._initialized:
            return
        
        logger.info("Initializing semantic analyzer...")
        
        try:
            # Load sentence transformer for semantic embeddings
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Load philosophical domains and their representative texts
            await self._load_philosophical_domains()
            
            # Generate domain embeddings
            await self._generate_domain_embeddings()
            
            self._initialized = True
            logger.info("Semantic analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize semantic analyzer: {e}")
            raise
    
    async def _load_philosophical_domains(self) -> None:
        """Load philosophical domains and their characteristic concepts."""
        self.philosophical_domains = {
            "ethics": [
                "moral responsibility", "virtue ethics", "consequentialism", "deontological ethics",
                "justice", "fairness", "rights", "duties", "moral dilemmas", "character",
                "good life", "human flourishing", "moral principles", "ethical theory"
            ],
            
            "metaphysics": [
                "reality", "existence", "being", "substance", "properties", "relations",
                "causation", "time", "space", "identity", "persistence", "possible worlds",
                "necessity", "contingency", "universals", "particulars"
            ],
            
            "epistemology": [
                "knowledge", "belief", "truth", "justification", "evidence", "skepticism",
                "certainty", "doubt", "perception", "memory", "testimony", "intuition",
                "reasoning", "inference", "empiricism", "rationalism"
            ],
            
            "philosophy_of_mind": [
                "consciousness", "mental states", "qualia", "intentionality", "mind-body problem",
                "dualism", "materialism", "functionalism", "behaviorism", "personal identity",
                "free will", "mental causation", "other minds"
            ],
            
            "political_philosophy": [
                "authority", "legitimacy", "liberty", "equality", "democracy", "justice",
                "social contract", "natural rights", "civil society", "state of nature",
                "political obligation", "civil disobedience", "distributive justice"
            ],
            
            "aesthetics": [
                "beauty", "art", "aesthetic experience", "taste", "judgment", "sublime",
                "artistic value", "aesthetic properties", "interpretation", "criticism",
                "artistic creation", "aesthetic theory"
            ],
            
            "philosophy_of_language": [
                "meaning", "reference", "truth conditions", "speech acts", "pragmatics",
                "semantics", "syntax", "language games", "private language", "translation",
                "interpretation", "communication"
            ],
            
            "philosophy_of_science": [
                "scientific method", "explanation", "laws of nature", "causation", "induction",
                "confirmation", "falsification", "scientific realism", "paradigms",
                "scientific revolutions", "objectivity", "measurement"
            ],
            
            "existentialism": [
                "existence", "essence", "authenticity", "bad faith", "freedom", "responsibility",
                "anxiety", "absurd", "nausea", "being-toward-death", "thrownness", "facticity",
                "existential analysis", "authentic existence"
            ],
            
            "eastern_philosophy": [
                "dharma", "karma", "enlightenment", "suffering", "impermanence", "no-self",
                "mindfulness", "meditation", "compassion", "wisdom", "tao", "wu wei",
                "yin yang", "qi", "li", "ren", "confucian virtues"
            ]
        }
    
    async def _generate_domain_embeddings(self) -> None:
        """Generate embeddings for philosophical domains."""
        for domain, concepts in self.philosophical_domains.items():
            # Create representative text for the domain
            domain_text = " ".join(concepts)
            
            # Generate embedding
            embedding = self.sentence_model.encode([domain_text])
            self.domain_embeddings[domain] = embedding[0]
    
    async def analyze_semantics(
        self, 
        text: str, 
        doc: spacy.Doc, 
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform comprehensive semantic analysis of philosophical text."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Generate text embedding
            text_embedding = self.sentence_model.encode([text])[0]
            
            # Analyze philosophical domain alignment
            domain_analysis = self._analyze_domain_alignment(text_embedding)
            
            # Extract key semantic relationships
            semantic_relations = self._extract_semantic_relations(doc)
            
            # Analyze conceptual coherence
            coherence_analysis = self._analyze_conceptual_coherence(text, doc)
            
            # Identify semantic themes
            semantic_themes = self._identify_semantic_themes(text, doc)
            
            # Analyze argument structure
            argument_structure = self._analyze_argument_structure(doc)
            
            # Calculate semantic complexity
            complexity_analysis = self._analyze_semantic_complexity(doc, text_embedding)
            
            return {
                "domain_alignment": domain_analysis,
                "semantic_relations": semantic_relations,
                "conceptual_coherence": coherence_analysis,
                "semantic_themes": semantic_themes,
                "argument_structure": argument_structure,
                "semantic_complexity": complexity_analysis,
                "text_embedding": text_embedding.tolist()[:50],  # First 50 dims for storage
                "overall_semantic_score": self._calculate_semantic_score(
                    domain_analysis, coherence_analysis, complexity_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Error in semantic analysis: {e}")
            return {"error": f"Semantic analysis failed: {str(e)}"}
    
    def _analyze_domain_alignment(self, text_embedding: np.ndarray) -> Dict[str, Any]:
        """Analyze alignment with philosophical domains."""
        domain_scores = {}
        
        for domain, domain_embedding in self.domain_embeddings.items():
            # Calculate cosine similarity
            similarity = cosine_similarity(
                text_embedding.reshape(1, -1), 
                domain_embedding.reshape(1, -1)
            )[0][0]
            
            domain_scores[domain] = float(similarity)
        
        # Sort by alignment strength
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "domain_scores": domain_scores,
            "primary_domain": sorted_domains[0][0] if sorted_domains else "general",
            "domain_confidence": sorted_domains[0][1] if sorted_domains else 0.0,
            "multi_domain": len([s for s in domain_scores.values() if s > 0.3]) > 1,
            "top_domains": [d[0] for d in sorted_domains[:3]]
        }
    
    def _extract_semantic_relations(self, doc: spacy.Doc) -> Dict[str, Any]:
        """Extract semantic relationships between concepts."""
        relations = []
        
        # Extract dependency relations of interest
        philosophical_relations = []
        for token in doc:
            # Subject-predicate-object relations
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                subject = token.text
                predicate = token.head.text
                
                # Find object if exists
                obj = None
                for child in token.head.children:
                    if child.dep_ in ["dobj", "pobj"]:
                        obj = child.text
                        break
                
                if obj:
                    philosophical_relations.append({
                        "type": "spo",
                        "subject": subject,
                        "predicate": predicate,
                        "object": obj
                    })
        
        # Extract noun-noun relationships
        noun_relations = []
        for token in doc:
            if token.pos_ == "NOUN":
                for child in token.children:
                    if child.pos_ == "NOUN" and child.dep_ in ["compound", "appos"]:
                        noun_relations.append({
                            "type": "noun_compound",
                            "head": token.text,
                            "modifier": child.text
                        })
        
        # Extract causal relations
        causal_relations = []
        causal_markers = ["because", "since", "due to", "results in", "leads to", "causes"]
        for sent in doc.sents:
            sent_text = sent.text.lower()
            for marker in causal_markers:
                if marker in sent_text:
                    causal_relations.append({
                        "type": "causal",
                        "marker": marker,
                        "sentence": sent.text
                    })
        
        return {
            "philosophical_relations": philosophical_relations[:10],  # Limit for performance
            "noun_relations": noun_relations[:10],
            "causal_relations": causal_relations[:5],
            "total_relations": len(philosophical_relations) + len(noun_relations) + len(causal_relations)
        }
    
    def _analyze_conceptual_coherence(self, text: str, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze coherence and consistency of concepts."""
        # Extract key concepts (nouns and noun phrases)
        concepts = []
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Limit to reasonable concept length
                concepts.append(chunk.text.lower().strip())
        
        if len(concepts) < 2:
            return {"coherence_score": 5.0, "concept_count": len(concepts)}
        
        # Generate embeddings for concepts
        try:
            concept_embeddings = self.sentence_model.encode(concepts)
            
            # Calculate pairwise similarities
            similarities = cosine_similarity(concept_embeddings)
            
            # Get average similarity (excluding self-similarities)
            n_concepts = len(concepts)
            total_similarity = 0
            count = 0
            
            for i in range(n_concepts):
                for j in range(i + 1, n_concepts):
                    total_similarity += similarities[i][j]
                    count += 1
            
            avg_similarity = total_similarity / count if count > 0 else 0
            
            # Convert to coherence score (0-10)
            coherence_score = min(10, max(0, avg_similarity * 10 + 5))
            
            return {
                "coherence_score": round(coherence_score, 1),
                "concept_count": len(concepts),
                "avg_concept_similarity": round(avg_similarity, 3),
                "concepts": concepts[:10]  # Show first 10 concepts
            }
            
        except Exception as e:
            logger.error(f"Error in coherence analysis: {e}")
            return {"coherence_score": 5.0, "concept_count": len(concepts)}
    
    def _identify_semantic_themes(self, text: str, doc: spacy.Doc) -> Dict[str, Any]:
        """Identify semantic themes using topic modeling techniques."""
        # Simple theme identification based on word clusters
        sentences = [sent.text for sent in doc.sents]
        
        if len(sentences) < 2:
            return {"themes": [], "theme_count": 0}
        
        try:
            # Generate sentence embeddings
            sentence_embeddings = self.sentence_model.encode(sentences)
            
            # Simple clustering approach - find most representative sentences
            # Calculate centroid
            centroid = np.mean(sentence_embeddings, axis=0)
            
            # Find sentences closest to centroid (main themes)
            similarities_to_centroid = cosine_similarity(
                sentence_embeddings, 
                centroid.reshape(1, -1)
            ).flatten()
            
            # Get top sentences as theme representatives
            top_indices = np.argsort(similarities_to_centroid)[-3:]  # Top 3
            themes = [sentences[i] for i in top_indices]
            
            return {
                "themes": themes,
                "theme_count": len(themes),
                "thematic_coherence": round(float(np.mean(similarities_to_centroid)), 3)
            }
            
        except Exception as e:
            logger.error(f"Error in theme identification: {e}")
            return {"themes": [], "theme_count": 0}
    
    def _analyze_argument_structure(self, doc: spacy.Doc) -> Dict[str, Any]:
        """Analyze logical argument structure in the text."""
        argument_indicators = {
            "premises": ["because", "since", "given that", "assuming", "if", "suppose"],
            "conclusions": ["therefore", "thus", "hence", "consequently", "so", "it follows"],
            "counterarguments": ["however", "but", "although", "yet", "on the other hand"],
            "support": ["furthermore", "moreover", "additionally", "also", "indeed"],
            "qualifiers": ["probably", "likely", "possibly", "might", "perhaps", "maybe"]
        }
        
        text_lower = doc.text.lower()
        
        # Count argument structure indicators
        structure_analysis = {}
        for category, indicators in argument_indicators.items():
            count = sum(text_lower.count(indicator) for indicator in indicators)
            structure_analysis[category] = count
        
        # Identify logical connectors
        logical_connectors = []
        for sent in doc.sents:
            sent_text = sent.text.lower()
            for category, indicators in argument_indicators.items():
                for indicator in indicators:
                    if indicator in sent_text:
                        logical_connectors.append({
                            "type": category,
                            "indicator": indicator,
                            "sentence": sent.text[:100] + "..." if len(sent.text) > 100 else sent.text
                        })
        
        # Calculate argument structure score
        total_indicators = sum(structure_analysis.values())
        sentence_count = len(list(doc.sents))
        argument_density = total_indicators / sentence_count if sentence_count > 0 else 0
        
        # Score based on presence of different types of indicators
        structure_variety = len([count for count in structure_analysis.values() if count > 0])
        structure_score = min(10, argument_density * 10 + structure_variety)
        
        return {
            "structure_score": round(structure_score, 1),
            "structure_analysis": structure_analysis,
            "logical_connectors": logical_connectors[:10],  # Limit for performance
            "argument_density": round(argument_density, 3),
            "structure_variety": structure_variety
        }
    
    def _analyze_semantic_complexity(
        self, 
        doc: spacy.Doc, 
        text_embedding: np.ndarray
    ) -> Dict[str, Any]:
        """Analyze semantic complexity of the text."""
        # Lexical diversity
        words = [token.lemma_.lower() for token in doc if token.is_alpha and not token.is_stop]
        unique_words = set(words)
        lexical_diversity = len(unique_words) / len(words) if words else 0
        
        # Sentence complexity (average dependency depth)
        dependency_depths = []
        for sent in doc.sents:
            max_depth = 0
            for token in sent:
                depth = self._calculate_dependency_depth(token)
                max_depth = max(max_depth, depth)
            dependency_depths.append(max_depth)
        
        avg_dependency_depth = sum(dependency_depths) / len(dependency_depths) if dependency_depths else 0
        
        # Semantic density (using embedding magnitude as proxy)
        semantic_density = float(np.linalg.norm(text_embedding))
        
        # Abstract concept density
        abstract_words = ["concept", "idea", "theory", "principle", "essence", "nature", "reality"]
        abstract_count = sum(doc.text.lower().count(word) for word in abstract_words)
        abstract_density = abstract_count / len(words) if words else 0
        
        # Overall complexity score
        complexity_score = min(10, 
            lexical_diversity * 3 +
            (avg_dependency_depth / 3) * 2 +
            (semantic_density / 10) * 2 +
            abstract_density * 10 * 3
        )
        
        return {
            "complexity_score": round(complexity_score, 1),
            "lexical_diversity": round(lexical_diversity, 3),
            "avg_dependency_depth": round(avg_dependency_depth, 1),
            "semantic_density": round(semantic_density, 2),
            "abstract_density": round(abstract_density, 3),
            "unique_word_count": len(unique_words),
            "total_word_count": len(words)
        }
    
    def _calculate_dependency_depth(self, token: spacy.Token, depth: int = 0) -> int:
        """Calculate maximum dependency depth from a token."""
        if not list(token.children):
            return depth
        
        max_child_depth = 0
        for child in token.children:
            child_depth = self._calculate_dependency_depth(child, depth + 1)
            max_child_depth = max(max_child_depth, child_depth)
        
        return max_child_depth
    
    def _calculate_semantic_score(
        self,
        domain_analysis: Dict[str, Any],
        coherence_analysis: Dict[str, Any],
        complexity_analysis: Dict[str, Any]
    ) -> float:
        """Calculate overall semantic analysis score."""
        # Weight different components
        domain_score = domain_analysis.get("domain_confidence", 0) * 10
        coherence_score = coherence_analysis.get("coherence_score", 5)
        complexity_score = complexity_analysis.get("complexity_score", 5)
        
        # Calculate weighted average
        overall_score = (domain_score * 0.3 + coherence_score * 0.4 + complexity_score * 0.3)
        
        return round(min(10, max(1, overall_score)), 1)
    
    async def find_similar_concepts(
        self, 
        concept: str, 
        threshold: float = 0.7
    ) -> List[Tuple[str, float]]:
        """Find concepts similar to the given concept."""
        if not self._initialized:
            await self.initialize()
        
        try:
            # Generate embedding for input concept
            concept_embedding = self.sentence_model.encode([concept])
            
            # Compare with all domain concepts
            similar_concepts = []
            for domain, concepts in self.philosophical_domains.items():
                domain_embeddings = self.sentence_model.encode(concepts)
                similarities = cosine_similarity(concept_embedding, domain_embeddings)[0]
                
                for i, similarity in enumerate(similarities):
                    if similarity > threshold:
                        similar_concepts.append((concepts[i], float(similarity)))
            
            # Sort by similarity
            similar_concepts.sort(key=lambda x: x[1], reverse=True)
            
            return similar_concepts[:10]  # Return top 10
            
        except Exception as e:
            logger.error(f"Error finding similar concepts: {e}")
            return []