export interface PhilosophyQuote {
  id: string
  quote: string
  author: string
  tradition: string
  context: string
  reflection: string
  themes: string[]
}

export const philosophyQuotes: PhilosophyQuote[] = [
  {
    id: 'stoic-marcus-1',
    quote: "You have power over your mind - not outside events. Realize this, and you will find strength.",
    author: "Marcus Aurelius",
    tradition: "Stoicism",
    context: "From his personal journal 'Meditations', written during his time as Roman Emperor.",
    reflection: "This reminds us that while we cannot control external circumstances, we always have sovereignty over our thoughts and responses.",
    themes: ["control", "inner strength", "resilience", "mindfulness"]
  },
  {
    id: 'buddhist-buddha-1',
    quote: "The mind is everything. What you think you become.",
    author: "Buddha",
    tradition: "Buddhism",
    context: "A fundamental teaching on the power of consciousness and mental cultivation.",
    reflection: "Our thoughts shape our reality, making mindfulness and intentional thinking crucial practices.",
    themes: ["mindfulness", "consciousness", "transformation", "mental cultivation"]
  },
  {
    id: 'existentialist-sartre-1',
    quote: "Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.",
    author: "Jean-Paul Sartre",
    tradition: "Existentialism",
    context: "From 'Being and Nothingness', exploring the nature of human freedom and responsibility.",
    reflection: "Freedom comes with the weight of responsibility - we are the authors of our own existence.",
    themes: ["freedom", "responsibility", "authenticity", "choice"]
  },
  {
    id: 'taoist-laozi-1',
    quote: "The Tao that can be told is not the eternal Tao.",
    author: "Lao Tzu",
    tradition: "Taoism",
    context: "Opening line of the Tao Te Ching, pointing to the ineffable nature of ultimate reality.",
    reflection: "Some truths transcend language and conceptual understanding - they must be experienced directly.",
    themes: ["mystery", "ineffability", "direct experience", "wisdom"]
  },
  {
    id: 'greek-socrates-1',
    quote: "The only true wisdom is in knowing you know nothing.",
    author: "Socrates",
    tradition: "Ancient Greek Philosophy",
    context: "Socratic wisdom emphasizes intellectual humility and the recognition of our limitations.",
    reflection: "True learning begins with acknowledging what we don't know and remaining open to new understanding.",
    themes: ["humility", "wisdom", "learning", "curiosity"]
  }
]

export const getRandomQuote = (tradition?: string): PhilosophyQuote => {
  let filteredQuotes = philosophyQuotes
  if (tradition) {
    filteredQuotes = philosophyQuotes.filter(q => 
      q.tradition.toLowerCase().includes(tradition.toLowerCase())
    )
  }
  
  if (filteredQuotes.length === 0) {
    filteredQuotes = philosophyQuotes
  }
  
  const randomIndex = Math.floor(Math.random() * filteredQuotes.length)
  return filteredQuotes[randomIndex]
}

export const getDailyQuote = (): PhilosophyQuote => {
  // Use date as seed for consistent daily quote
  const today = new Date()
  const seed = today.getDate() + today.getMonth() * 31 + today.getFullYear() * 365
  const index = seed % philosophyQuotes.length
  return philosophyQuotes[index]
}

export const getQuotesByTradition = (tradition: string): PhilosophyQuote[] => {
  return philosophyQuotes.filter(q => 
    q.tradition.toLowerCase().includes(tradition.toLowerCase())
  )
}

export const getQuotesByTheme = (theme: string): PhilosophyQuote[] => {
  return philosophyQuotes.filter(q => 
    q.themes.some(t => t.toLowerCase().includes(theme.toLowerCase()))
  )
}

export const getAllTraditions = (): string[] => {
  return [...new Set(philosophyQuotes.map(q => q.tradition))]
}