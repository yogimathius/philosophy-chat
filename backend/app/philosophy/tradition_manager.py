"""Manager for different philosophical traditions and their characteristics."""

import asyncio
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TraditionManager:
    """Manage multiple philosophical traditions and their characteristics."""
    
    def __init__(self):
        """Initialize tradition manager."""
        self.traditions: Dict[str, Dict[str, Any]] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize tradition manager with philosophical traditions."""
        if self._initialized:
            return
        
        logger.info("Initializing tradition manager...")
        
        try:
            await self._load_philosophical_traditions()
            self._initialized = True
            logger.info("Tradition manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize tradition manager: {e}")
            raise
    
    async def _load_philosophical_traditions(self) -> None:
        """Load comprehensive philosophical tradition data."""
        
        self.traditions = {
            "stoicism": {
                "name": "Stoicism",
                "description": "Ancient philosophy emphasizing virtue, wisdom, and emotional resilience",
                "core_principles": [
                    "Focus on what you can control",
                    "Live according to nature",
                    "Virtue is the only true good",
                    "Accept what cannot be changed",
                    "Practice negative visualization"
                ],
                "key_thinkers": [
                    {"name": "Marcus Aurelius", "period": "121-180 CE", "role": "Roman Emperor-Philosopher"},
                    {"name": "Epictetus", "period": "50-135 CE", "role": "Former slave, teacher"},
                    {"name": "Seneca", "period": "4 BCE-65 CE", "role": "Roman statesman, writer"},
                    {"name": "Zeno of Citium", "period": "334-262 BCE", "role": "Founder of Stoicism"}
                ],
                "prompt_style": """You are a wise Stoic philosopher in the tradition of Marcus Aurelius, Epictetus, and Seneca. 
                
CORE STOIC PRINCIPLES:
- Focus on what is within our control (our judgments, values, and responses) vs. what is not (external events, others' actions)
- Live according to nature - both human nature as rational beings and cosmic nature
- Virtue (wisdom, justice, courage, temperance) is the only true good
- External things are "indifferent" - neither good nor bad in themselves
- Practice amor fati - love of one's fate, accepting what happens
                
STOIC APPROACH:
- Guide the person to examine what is truly under their control
- Encourage practical wisdom (phronesis) in daily decisions  
- Help reframe challenges as opportunities for virtue practice
- Emphasize present-moment awareness and rational response
- Use exercises like negative visualization, evening reflection, morning preparation
                
TONE: Calm, wise, practical, encouraging resilience while being compassionate""",
                
                "model_parameters": {
                    "temperature": 0.6,
                    "max_tokens": 800,
                    "presence_penalty": 0.1,
                    "frequency_penalty": 0.1
                },
                
                "reading_suggestions": {
                    "beginner": [
                        {"title": "Meditations", "author": "Marcus Aurelius", "reason": "Personal reflections of a practicing Stoic"},
                        {"title": "The Enchiridion", "author": "Epictetus", "reason": "Concise handbook of Stoic principles"},
                        {"title": "Letters from a Stoic", "author": "Seneca", "reason": "Practical wisdom for daily life"}
                    ],
                    "intermediate": [
                        {"title": "Discourses", "author": "Epictetus", "reason": "Deeper exploration of Stoic psychology"},
                        {"title": "A Guide to the Good Life", "author": "William Irvine", "reason": "Modern application of Stoic practices"}
                    ],
                    "advanced": [
                        {"title": "The Stoic Way of Life", "author": "Tad Brennan", "reason": "Scholarly examination of Stoic philosophy"}
                    ]
                }
            },
            
            "existentialism": {
                "name": "Existentialism", 
                "description": "Philosophy emphasizing individual existence, freedom, and choice",
                "core_principles": [
                    "Existence precedes essence",
                    "Radical freedom and responsibility",
                    "Authenticity vs. bad faith",
                    "Creating meaning in an absurd world",
                    "Embracing anxiety as awareness of freedom"
                ],
                "key_thinkers": [
                    {"name": "Jean-Paul Sartre", "period": "1905-1980", "role": "French philosopher, playwright"},
                    {"name": "Simone de Beauvoir", "period": "1908-1986", "role": "Feminist existentialist"},
                    {"name": "Albert Camus", "period": "1913-1960", "role": "Absurdist philosopher, writer"},
                    {"name": "Søren Kierkegaard", "period": "1813-1855", "role": "Danish proto-existentialist"},
                    {"name": "Martin Heidegger", "period": "1889-1976", "role": "German phenomenologist"}
                ],
                "prompt_style": """You are an existentialist philosopher inspired by Sartre, de Beauvoir, Camus, and Kierkegaard.
                
CORE EXISTENTIALIST THEMES:
- Existence precedes essence - we exist first, then create our nature through choices
- Radical freedom and the weight of responsibility that comes with it
- Authenticity vs. bad faith - living genuinely vs. self-deception
- The absurd condition of human existence seeking meaning in a meaningless universe
- Anxiety (anguish) as the dizziness of freedom when facing choices
                
EXISTENTIALIST APPROACH:
- Help people recognize their fundamental freedom and responsibility
- Explore the tension between freedom and the weight of choice
- Encourage authentic existence rather than conformity to social roles
- Examine bad faith - the ways we deceive ourselves about our freedom
- Address the anxiety that comes with recognizing our radical responsibility
- Explore how to create meaning and values in an absurd world
                
TONE: Intense, authentic, challenging, sometimes provocative, always honest about the difficulty of human existence""",
                
                "model_parameters": {
                    "temperature": 0.8,
                    "max_tokens": 800,
                    "presence_penalty": 0.3,
                    "frequency_penalty": 0.2
                },
                
                "reading_suggestions": {
                    "beginner": [
                        {"title": "The Stranger", "author": "Albert Camus", "reason": "Accessible exploration of absurdism"},
                        {"title": "Existentialism is a Humanism", "author": "Jean-Paul Sartre", "reason": "Clear introduction to existentialist ideas"}
                    ],
                    "intermediate": [
                        {"title": "Being and Nothingness", "author": "Jean-Paul Sartre", "reason": "Major work on freedom and bad faith"},
                        {"title": "The Ethics of Ambiguity", "author": "Simone de Beauvoir", "reason": "Existentialist ethics and responsibility"}
                    ],
                    "advanced": [
                        {"title": "Being and Time", "author": "Martin Heidegger", "reason": "Fundamental ontology and authentic existence"}
                    ]
                }
            },
            
            "buddhism": {
                "name": "Buddhism",
                "description": "Ancient wisdom tradition focused on liberation from suffering",
                "core_principles": [
                    "Four Noble Truths",
                    "Eightfold Path",
                    "Three Jewels (Buddha, Dharma, Sangha)",
                    "Impermanence (anicca)",
                    "No-self (anatman)",
                    "Interdependence",
                    "Mindfulness and meditation"
                ],
                "key_thinkers": [
                    {"name": "Siddhartha Gautama (Buddha)", "period": "563-483 BCE", "role": "Founder of Buddhism"},
                    {"name": "Nagarjuna", "period": "150-250 CE", "role": "Madhyamaka philosopher"},
                    {"name": "Thich Nhat Hanh", "period": "1926-2022", "role": "Vietnamese Zen master"},
                    {"name": "Dalai Lama XIV", "period": "1935-present", "role": "Tibetan Buddhist leader"}
                ],
                "prompt_style": """You are a Buddhist teacher in the tradition of mindfulness, compassion, and wisdom.
                
CORE BUDDHIST TEACHINGS:
- Four Noble Truths: suffering exists, has a cause (craving/attachment), can end, path to end it
- Eightfold Path: right understanding, intention, speech, action, livelihood, effort, mindfulness, concentration
- Three marks of existence: impermanence, suffering, no-self
- Interdependence: all phenomena arise in dependence upon causes and conditions
- Middle Way: avoiding extremes of indulgence and severe asceticism
                
BUDDHIST APPROACH:
- Guide toward understanding the nature of suffering and its causes
- Encourage mindful awareness of present-moment experience
- Explore attachment and aversion as sources of suffering
- Cultivate compassion for self and all beings
- Practice non-judgment and acceptance
- Investigate the illusion of a fixed, separate self
- Emphasize practical meditation and mindfulness techniques
                
TONE: Compassionate, gentle, patient, wise, non-dogmatic, emphasizing direct experience over belief""",
                
                "model_parameters": {
                    "temperature": 0.5,
                    "max_tokens": 800,
                    "presence_penalty": 0.1,
                    "frequency_penalty": 0.0
                },
                
                "reading_suggestions": {
                    "beginner": [
                        {"title": "The Heart of Buddhist Meditation", "author": "Nyanaponika Thera", "reason": "Clear guide to mindfulness practice"},
                        {"title": "Buddhism Without Beliefs", "author": "Stephen Batchelor", "reason": "Accessible, non-religious approach"}
                    ],
                    "intermediate": [
                        {"title": "The Middle Length Discourses", "author": "Buddha (translated)", "reason": "Core Buddhist teachings"},
                        {"title": "Being Nobody, Going Nowhere", "author": "Ayya Khema", "reason": "Practical wisdom for meditation"}
                    ],
                    "advanced": [
                        {"title": "The Fundamental Wisdom of the Middle Way", "author": "Nagarjuna", "reason": "Profound exploration of emptiness"}
                    ]
                }
            },
            
            "socratic": {
                "name": "Socratic Method",
                "description": "Philosophical inquiry through questioning and dialogue",
                "core_principles": [
                    "Knowledge through questioning",
                    "\"I know that I know nothing\"",
                    "The unexamined life is not worth living",
                    "Virtue is knowledge",
                    "Care of the soul",
                    "Dialectical reasoning"
                ],
                "key_thinkers": [
                    {"name": "Socrates", "period": "470-399 BCE", "role": "Father of Western philosophy"},
                    {"name": "Plato", "period": "428-348 BCE", "role": "Student of Socrates, dialogues"},
                    {"name": "Aristotle", "period": "384-322 BCE", "role": "Student of Plato, systematic philosophy"}
                ],
                "prompt_style": """You are Socrates, the gadfly of Athens, committed to examining life through dialogue.
                
SOCRATIC PRINCIPLES:
- \"The only thing I know is that I know nothing\" - intellectual humility
- Questions are more valuable than answers
- The unexamined life is not worth living
- Virtue and knowledge are connected
- Truth emerges through dialogue and questioning
- Challenge assumptions and conventional wisdom
                
SOCRATIC METHOD:
- Ask probing questions rather than providing direct answers
- Help people examine their beliefs and assumptions  
- Use analogies and examples to clarify thinking
- Expose contradictions in reasoning
- Guide toward self-discovery rather than teaching directly
- Show that apparent knowledge often masks ignorance
- Maintain intellectual humility while persistent inquiry
                
TONE: Curious, humble, persistent, sometimes playfully ironic, always genuinely interested in truth""",
                
                "model_parameters": {
                    "temperature": 0.7,
                    "max_tokens": 700,
                    "presence_penalty": 0.2,
                    "frequency_penalty": 0.1
                },
                
                "reading_suggestions": {
                    "beginner": [
                        {"title": "The Apology", "author": "Plato", "reason": "Socrates' defense of his philosophical life"},
                        {"title": "Meno", "author": "Plato", "reason": "Classic example of Socratic questioning"}
                    ],
                    "intermediate": [
                        {"title": "The Republic", "author": "Plato", "reason": "Extended Socratic dialogue on justice"},
                        {"title": "Phaedo", "author": "Plato", "reason": "Socrates on the soul and death"}
                    ],
                    "advanced": [
                        {"title": "Socratic Puzzles", "author": "Gregory Vlastos", "reason": "Scholarly analysis of Socratic philosophy"}
                    ]
                }
            },
            
            "eclectic": {
                "name": "Eclectic Philosophy",
                "description": "Drawing wisdom from multiple philosophical traditions",
                "core_principles": [
                    "Integration of diverse wisdom traditions",
                    "Pragmatic approach to truth",
                    "Cultural sensitivity and inclusivity",
                    "Adaptation to individual needs",
                    "Synthesis over dogma"
                ],
                "key_thinkers": [
                    {"name": "William James", "period": "1842-1910", "role": "American pragmatist"},
                    {"name": "John Dewey", "period": "1859-1952", "role": "Pragmatic philosopher"},
                    {"name": "Martha Nussbaum", "period": "1947-present", "role": "Contemporary philosopher"}
                ],
                "prompt_style": """You are a wise philosophical guide who draws from multiple wisdom traditions around the world.
                
ECLECTIC APPROACH:
- Draw from various philosophical traditions as appropriate to the question
- Respect the diversity of human wisdom across cultures and time periods
- Adapt your approach to the individual's needs, background, and interests
- Synthesize insights rather than adhering to any single doctrine
- Show how different traditions might address the same question
- Encourage exploration of multiple perspectives
                
TRADITIONS TO DRAW FROM:
- Western philosophy (Ancient Greek, Medieval, Modern, Contemporary)
- Eastern wisdom (Buddhism, Hinduism, Taoism, Confucianism)
- Indigenous philosophies from various cultures
- Contemporary movements (existentialism, pragmatism, analytic philosophy)
- Practical philosophy and applied ethics
                
TONE: Open-minded, culturally sensitive, intellectually curious, integrative, humble about the limits of any single perspective""",
                
                "model_parameters": {
                    "temperature": 0.7,
                    "max_tokens": 850,
                    "presence_penalty": 0.2,
                    "frequency_penalty": 0.1
                },
                
                "reading_suggestions": {
                    "beginner": [
                        {"title": "The World's Religions", "author": "Huston Smith", "reason": "Survey of global wisdom traditions"},
                        {"title": "Philosophy: A Very Short Introduction", "author": "Edward Craig", "reason": "Overview of philosophical thinking"}
                    ],
                    "intermediate": [
                        {"title": "The Consolations of Philosophy", "author": "Alain de Botton", "reason": "Practical wisdom from various thinkers"},
                        {"title": "Justice", "author": "Michael Sandel", "reason": "Examining moral questions through multiple lenses"}
                    ],
                    "advanced": [
                        {"title": "Sources of the Self", "author": "Charles Taylor", "reason": "Contemporary synthesis of identity and morality"}
                    ]
                }
            }
        }
    
    async def get_tradition_prompt(self, tradition: str) -> str:
        """Get the system prompt for a specific tradition."""
        if not self._initialized:
            await self.initialize()
        
        tradition_data = self.traditions.get(tradition)
        if not tradition_data:
            tradition_data = self.traditions["eclectic"]
        
        return tradition_data["prompt_style"]
    
    async def get_model_parameters(self, tradition: str) -> Dict[str, Any]:
        """Get AI model parameters optimized for a tradition."""
        if not self._initialized:
            await self.initialize()
        
        tradition_data = self.traditions.get(tradition)
        if not tradition_data:
            tradition_data = self.traditions["eclectic"]
        
        return tradition_data["model_parameters"]
    
    async def get_reading_suggestions(
        self, 
        tradition: str, 
        concepts: List[str], 
        level: str = "intermediate"
    ) -> List[Dict[str, str]]:
        """Get reading suggestions for a tradition and concepts."""
        if not self._initialized:
            await self.initialize()
        
        tradition_data = self.traditions.get(tradition)
        if not tradition_data:
            return []
        
        suggestions = tradition_data.get("reading_suggestions", {}).get(level, [])
        
        # Filter or modify suggestions based on concepts if needed
        # For now, return the base suggestions
        return suggestions
    
    async def get_tradition_info(self, tradition: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive information about a tradition."""
        if not self._initialized:
            await self.initialize()
        
        return self.traditions.get(tradition)
    
    async def list_available_traditions(self) -> List[Dict[str, str]]:
        """List all available philosophical traditions."""
        if not self._initialized:
            await self.initialize()
        
        return [
            {
                "key": key,
                "name": data["name"],
                "description": data["description"]
            }
            for key, data in self.traditions.items()
        ]
    
    async def suggest_tradition(self, user_interests: List[str]) -> str:
        """Suggest a philosophical tradition based on user interests."""
        if not self._initialized:
            await self.initialize()
        
        # Simple mapping of interests to traditions
        interest_mapping = {
            "resilience": "stoicism",
            "stress": "stoicism", 
            "control": "stoicism",
            "virtue": "stoicism",
            "freedom": "existentialism",
            "authenticity": "existentialism",
            "meaning": "existentialism",
            "responsibility": "existentialism",
            "mindfulness": "buddhism",
            "suffering": "buddhism",
            "meditation": "buddhism",
            "compassion": "buddhism",
            "questioning": "socratic",
            "dialogue": "socratic",
            "knowledge": "socratic",
            "truth": "socratic",
        }
        
        # Count matches for each tradition
        tradition_scores = {}
        for interest in user_interests:
            interest_lower = interest.lower()
            for keyword, tradition in interest_mapping.items():
                if keyword in interest_lower:
                    tradition_scores[tradition] = tradition_scores.get(tradition, 0) + 1
        
        if tradition_scores:
            return max(tradition_scores.items(), key=lambda x: x[1])[0]
        
        return "eclectic"  # Default fallback
    
    async def get_tradition_practices(self, tradition: str) -> List[Dict[str, str]]:
        """Get practical exercises/practices for a tradition."""
        practices = {
            "stoicism": [
                {
                    "name": "Morning Reflection",
                    "description": "Begin each day by considering what is and isn't under your control",
                    "instructions": "Spend 5-10 minutes each morning reflecting on the day ahead, identifying what you can and cannot control"
                },
                {
                    "name": "Evening Review", 
                    "description": "End each day by examining your thoughts, actions, and responses",
                    "instructions": "Before sleep, review the day: What went well? Where could you have responded more virtuously?"
                },
                {
                    "name": "Negative Visualization",
                    "description": "Imagine losing what you value to increase gratitude and prepare for loss",
                    "instructions": "Briefly imagine losing something you value, then return to appreciating what you have"
                }
            ],
            "buddhism": [
                {
                    "name": "Mindful Breathing",
                    "description": "Focus attention on the breath to cultivate present-moment awareness",
                    "instructions": "Sit quietly and focus on your breath. When the mind wanders, gently return attention to breathing"
                },
                {
                    "name": "Loving-Kindness Meditation",
                    "description": "Cultivate compassion for yourself and others",
                    "instructions": "Silently repeat: 'May I be happy, may I be peaceful, may I be free from suffering' then extend to others"
                },
                {
                    "name": "Impermanence Reflection",
                    "description": "Contemplate the temporary nature of all phenomena",
                    "instructions": "Observe how everything changes - thoughts, sensations, emotions - nothing remains the same"
                }
            ],
            "existentialism": [
                {
                    "name": "Authenticity Check",
                    "description": "Examine whether you're living authentically or in bad faith",
                    "instructions": "Ask yourself: 'Am I choosing this or just following others? What would I choose if no one was watching?'"
                },
                {
                    "name": "Freedom Recognition",
                    "description": "Acknowledge your radical freedom and responsibility",
                    "instructions": "In decision moments, pause and recognize: 'I am free to choose, and I am responsible for this choice'"
                },
                {
                    "name": "Meaning Creation",
                    "description": "Actively create meaning rather than seeking to find it",
                    "instructions": "Ask: 'What meaning can I create in this situation?' rather than 'What does this mean?'"
                }
            ]
        }
        
        return practices.get(tradition, [])