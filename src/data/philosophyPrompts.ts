export interface PhilosophyPrompt {
  id: string
  content: string
  tradition: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  theme: string
  author?: string
  context: string
  followUpQuestions: string[]
}

export const philosophyPrompts: PhilosophyPrompt[] = [
  // Stoicism - Beginner
  {
    id: 'stoic-001',
    content: 'What aspects of your daily life are within your control, and which are not?',
    tradition: 'Stoicism',
    difficulty: 'beginner',
    theme: 'Control and Acceptance',
    author: 'Epictetus',
    context: 'The fundamental Stoic principle of focusing only on what is within our control.',
    followUpQuestions: [
      'How does this realization change your approach to daily challenges?',
      'What happens when you focus energy on things outside your control?',
      'Can you think of a recent situation where this principle would have helped?'
    ]
  },
  {
    id: 'stoic-002',
    content: 'How can obstacles and setbacks become opportunities for growth?',
    tradition: 'Stoicism',
    difficulty: 'beginner',
    theme: 'Resilience',
    author: 'Marcus Aurelius',
    context: 'The Stoic concept that impediments to action advance action, and obstacles become the way.',
    followUpQuestions: [
      'What is a current challenge that could teach you something valuable?',
      'How might your perspective on problems change if you saw them as training?',
      'What strengths have you developed through past difficulties?'
    ]
  },
  
  // Buddhism - Beginner
  {
    id: 'buddhist-001',
    content: 'What attachments in your life cause you the most suffering?',
    tradition: 'Buddhism',
    difficulty: 'beginner',
    theme: 'Attachment and Suffering',
    context: 'The Second Noble Truth: attachment and craving are the root of suffering.',
    followUpQuestions: [
      'How do your expectations about outcomes affect your peace of mind?',
      'What would it feel like to hold your goals more lightly?',
      'Where do you notice grasping most strongly in your daily life?'
    ]
  },
  {
    id: 'buddhist-002',
    content: 'How does practicing mindful awareness change your relationship with thoughts and emotions?',
    tradition: 'Buddhism',
    difficulty: 'intermediate',
    theme: 'Mindfulness',
    context: 'The practice of observing mental phenomena without identification or judgment.',
    followUpQuestions: [
      'What do you notice when you observe thoughts without believing them?',
      'How does emotional reactivity change with mindful awareness?',
      'What patterns emerge when you watch your mind consistently?'
    ]
  },

  // Existentialism - Intermediate
  {
    id: 'existential-001',
    content: 'In a universe without predetermined meaning, how do you create purpose in your life?',
    tradition: 'Existentialism',
    difficulty: 'intermediate',
    theme: 'Meaning and Purpose',
    author: 'Jean-Paul Sartre',
    context: 'Existentialist concept that existence precedes essence - we create our own meaning.',
    followUpQuestions: [
      'What values do you choose to live by, and why?',
      'How does taking full responsibility for your choices feel?',
      'What meaning emerges from your authentic self-expression?'
    ]
  },
  {
    id: 'existential-002',
    content: 'What does it mean to live authentically versus conforming to others\' expectations?',
    tradition: 'Existentialism',
    difficulty: 'intermediate',
    theme: 'Authenticity',
    author: 'Søren Kierkegaard',
    context: 'The existentialist emphasis on individual authenticity and self-determination.',
    followUpQuestions: [
      'Where do you notice yourself conforming instead of being authentic?',
      'What would change if you prioritized authenticity over approval?',
      'How do societal roles and expectations shape your behavior?'
    ]
  },

  // Ancient Greek Philosophy - Beginner to Advanced
  {
    id: 'socratic-001',
    content: 'What do you think you know with certainty, and how do you know it?',
    tradition: 'Ancient Greek',
    difficulty: 'intermediate',
    theme: 'Knowledge and Wisdom',
    author: 'Socrates',
    context: 'Socratic method of questioning assumptions and examining the foundations of knowledge.',
    followUpQuestions: [
      'What beliefs have you never questioned but perhaps should?',
      'How do you distinguish between opinion and genuine knowledge?',
      'What would change if you approached life with more intellectual humility?'
    ]
  },
  {
    id: 'aristotelian-001',
    content: 'What does it mean to live a flourishing life (eudaimonia)?',
    tradition: 'Ancient Greek',
    difficulty: 'intermediate',
    theme: 'The Good Life',
    author: 'Aristotle',
    context: 'Aristotelian concept of eudaimonia as human flourishing through virtue and excellence.',
    followUpQuestions: [
      'What virtues do you most want to cultivate in yourself?',
      'How do you balance individual happiness with contributing to others?',
      'What activities make you feel most alive and fulfilled?'
    ]
  },

  // Modern Philosophy - Advanced
  {
    id: 'kantian-001',
    content: 'How do you determine what is morally right when facing difficult ethical decisions?',
    tradition: 'Modern Philosophy',
    difficulty: 'advanced',
    theme: 'Ethics and Morality',
    author: 'Immanuel Kant',
    context: 'Kantian ethics and the categorical imperative as a foundation for moral reasoning.',
    followUpQuestions: [
      'What principles guide your ethical decision-making?',
      'How do you balance consequences with moral duties?',
      'What would happen if everyone acted as you do in moral situations?'
    ]
  },

  // Eastern Philosophy - Various levels
  {
    id: 'taoism-001',
    content: 'How can you align with the natural flow of life rather than forcing outcomes?',
    tradition: 'Taoism',
    difficulty: 'beginner',
    theme: 'Wu Wei (Effortless Action)',
    author: 'Lao Tzu',
    context: 'Taoist principle of wu wei - acting in accordance with natural flow.',
    followUpQuestions: [
      'Where in your life are you pushing too hard against natural rhythms?',
      'What does effortless action feel like in practice?',
      'How do you distinguish between wise action and passive inaction?'
    ]
  },

  // Contemporary Philosophy
  {
    id: 'contemporary-001',
    content: 'How do you maintain meaning and connection in an increasingly digital world?',
    tradition: 'Contemporary',
    difficulty: 'intermediate',
    theme: 'Technology and Humanity',
    context: 'Modern questions about authentic human experience in the digital age.',
    followUpQuestions: [
      'What role does technology play in your sense of identity?',
      'How do digital interactions differ from embodied presence?',
      'What practices help you stay grounded in physical reality?'
    ]
  },

  // Applied Ethics
  {
    id: 'ethics-001',
    content: 'What responsibilities do you have toward future generations?',
    tradition: 'Applied Ethics',
    difficulty: 'intermediate',
    theme: 'Environmental Ethics',
    context: 'Contemporary questions about intergenerational justice and sustainability.',
    followUpQuestions: [
      'How do your daily choices impact future generations?',
      'What do you owe to people not yet born?',
      'How do you balance present needs with future consequences?'
    ]
  },

  // Practical Wisdom
  {
    id: 'practical-001',
    content: 'How do you cultivate wisdom in the midst of uncertainty and change?',
    tradition: 'Practical Wisdom',
    difficulty: 'intermediate',
    theme: 'Wisdom and Learning',
    context: 'The ongoing development of practical wisdom (phronesis) through experience.',
    followUpQuestions: [
      'What experiences have taught you the most about life?',
      'How do you learn from mistakes without being paralyzed by them?',
      'What does it mean to be wise versus merely intelligent?'
    ]
  },

  // Philosophy of Mind
  {
    id: 'consciousness-001',
    content: 'What is the relationship between your thoughts and your sense of self?',
    tradition: 'Philosophy of Mind',
    difficulty: 'advanced',
    theme: 'Consciousness and Identity',
    context: 'Questions about the nature of consciousness and personal identity.',
    followUpQuestions: [
      'Are you your thoughts, or do you observe your thoughts?',
      'What remains constant about you as everything else changes?',
      'How do you experience the gap between thoughts?'
    ]
  }
]

// Helper functions for filtering prompts
export const getPromptsByTradition = (tradition: string) => 
  philosophyPrompts.filter(prompt => prompt.tradition === tradition)

export const getPromptsByDifficulty = (difficulty: 'beginner' | 'intermediate' | 'advanced') =>
  philosophyPrompts.filter(prompt => prompt.difficulty === difficulty)

export const getPromptsByTheme = (theme: string) =>
  philosophyPrompts.filter(prompt => prompt.theme === theme)

export const getRandomPrompt = (tradition?: string, difficulty?: string) => {
  let filteredPrompts = philosophyPrompts
  
  if (tradition) {
    filteredPrompts = filteredPrompts.filter(prompt => prompt.tradition === tradition)
  }
  
  if (difficulty) {
    filteredPrompts = filteredPrompts.filter(prompt => prompt.difficulty === difficulty)
  }
  
  return filteredPrompts[Math.floor(Math.random() * filteredPrompts.length)]
}

export const getAllTraditions = () => 
  [...new Set(philosophyPrompts.map(prompt => prompt.tradition))]

export const getAllThemes = () =>
  [...new Set(philosophyPrompts.map(prompt => prompt.theme))]