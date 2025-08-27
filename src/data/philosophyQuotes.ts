export interface PhilosophyQuote {
  id: string
  quote: string
  author: string
  tradition: string
  theme: string
  context: string
  reflection: string
}

export const philosophyQuotes: PhilosophyQuote[] = [
  // Stoicism
  {
    id: 'quote-stoic-001',
    quote: 'You have power over your mind - not outside events. Realize this, and you will find strength.',
    author: 'Marcus Aurelius',
    tradition: 'Stoicism',
    theme: 'Control and Inner Peace',
    context: 'From "Meditations," written by the Roman Emperor as personal reflections on Stoic philosophy.',
    reflection: 'This reminds us that our greatest power lies not in controlling the world, but in choosing our responses to it.'
  },
  {
    id: 'quote-stoic-002',
    quote: 'It\'s not about what happens to you, but how you react to it that matters.',
    author: 'Epictetus',
    tradition: 'Stoicism',
    theme: 'Perspective and Response',
    context: 'Teaching from the former slave who became one of the greatest Stoic philosophers.',
    reflection: 'Our reactions shape our experience more than the events themselves. We always have the freedom to choose our response.'
  },
  {
    id: 'quote-stoic-003',
    quote: 'The impediment to action advances action. What stands in the way becomes the way.',
    author: 'Marcus Aurelius',
    tradition: 'Stoicism',
    theme: 'Resilience and Growth',
    context: 'A core Stoic principle that obstacles are opportunities for growth and strength.',
    reflection: 'Every challenge contains within it the seeds of our development. Resistance becomes our teacher.'
  },

  // Buddhism
  {
    id: 'quote-buddhist-001',
    quote: 'Pain is inevitable. Suffering is optional.',
    author: 'Buddha',
    tradition: 'Buddhism',
    theme: 'Suffering and Acceptance',
    context: 'Core Buddhist teaching on the difference between unavoidable pain and self-created suffering.',
    reflection: 'While we cannot avoid all pain, we can learn to not compound it with resistance, attachment, and mental stories.'
  },
  {
    id: 'quote-buddhist-002',
    quote: 'The mind is everything. What you think you become.',
    author: 'Buddha',
    tradition: 'Buddhism',
    theme: 'Mindfulness and Transformation',
    context: 'Teaching on the power of mental cultivation and conscious awareness.',
    reflection: 'Our thoughts shape our reality. By training the mind, we transform our entire experience of life.'
  },
  {
    id: 'quote-buddhist-003',
    quote: 'Be where you are; otherwise you will miss your life.',
    author: 'Buddha',
    tradition: 'Buddhism',
    theme: 'Present Moment Awareness',
    context: 'On the importance of mindfulness and presence in each moment.',
    reflection: 'Life happens now. When we\'re lost in past or future, we miss the only time we can actually live.'
  },

  // Ancient Greek Philosophy
  {
    id: 'quote-socratic-001',
    quote: 'The only true wisdom is in knowing you know nothing.',
    author: 'Socrates',
    tradition: 'Ancient Greek',
    theme: 'Wisdom and Humility',
    context: 'Socratic paradox emphasizing intellectual humility as the beginning of wisdom.',
    reflection: 'True learning begins when we acknowledge the limits of our knowledge. Humility opens the door to wisdom.'
  },
  {
    id: 'quote-aristotelian-001',
    quote: 'Knowing yourself is the beginning of all wisdom.',
    author: 'Aristotle',
    tradition: 'Ancient Greek',
    theme: 'Self-Knowledge',
    context: 'On the foundational importance of self-understanding in philosophical life.',
    reflection: 'All wisdom starts with honest self-examination. We cannot understand the world without first understanding ourselves.'
  },
  {
    id: 'quote-aristotelian-002',
    quote: 'We are what we repeatedly do. Excellence, then, is not an act, but a habit.',
    author: 'Aristotle',
    tradition: 'Ancient Greek',
    theme: 'Character and Virtue',
    context: 'From Nicomachean Ethics on the development of character through habitual practice.',
    reflection: 'Our character is formed by our consistent actions. Excellence emerges from disciplined practice over time.'
  },

  // Existentialism
  {
    id: 'quote-existential-001',
    quote: 'Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.',
    author: 'Jean-Paul Sartre',
    tradition: 'Existentialism',
    theme: 'Freedom and Responsibility',
    context: 'Core existentialist principle on radical freedom and the burden of choice.',
    reflection: 'Freedom is both our greatest gift and heaviest burden. With it comes complete responsibility for who we become.'
  },
  {
    id: 'quote-existential-002',
    quote: 'The most painful thing is losing yourself in the process of loving someone too much, and forgetting that you are special too.',
    author: 'Ernest Hemingway',
    tradition: 'Existentialism',
    theme: 'Authenticity and Self-Worth',
    context: 'On maintaining authentic selfhood while in relationship with others.',
    reflection: 'Love requires maintaining our own identity and worth. We cannot give what we do not possess within ourselves.'
  },

  // Taoism
  {
    id: 'quote-taoist-001',
    quote: 'The sage does not attempt anything very big, and thus achieves greatness.',
    author: 'Lao Tzu',
    tradition: 'Taoism',
    theme: 'Wu Wei and Natural Action',
    context: 'From the Tao Te Ching on the power of working with natural forces.',
    reflection: 'True greatness comes from aligning with natural rhythms rather than forcing outcomes through excessive effort.'
  },
  {
    id: 'quote-taoist-002',
    quote: 'Those who flow as life flows know they need no other force.',
    author: 'Lao Tzu',
    tradition: 'Taoism',
    theme: 'Flow and Harmony',
    context: 'Teaching on wu wei - effortless action in harmony with the Tao.',
    reflection: 'When we align with life\'s natural currents, we find power in surrender and strength in flexibility.'
  },

  // Modern Philosophy
  {
    id: 'quote-nietzsche-001',
    quote: 'What does not kill me, makes me stronger.',
    author: 'Friedrich Nietzsche',
    tradition: 'Modern Philosophy',
    theme: 'Resilience and Self-Overcoming',
    context: 'From "Twilight of the Idols" on the transformative power of challenges.',
    reflection: 'Adversity can be our teacher, building resilience and revealing strengths we didn\'t know we possessed.'
  },
  {
    id: 'quote-kantian-001',
    quote: 'Act only according to that maxim whereby you can at the same time will that it should become a universal law.',
    author: 'Immanuel Kant',
    tradition: 'Modern Philosophy',
    theme: 'Ethics and Universal Principles',
    context: 'The categorical imperative from "Groundwork for the Metaphysics of Morals."',
    reflection: 'Ethical action considers not just personal benefit, but what would happen if everyone acted the same way.'
  },

  // Contemporary Wisdom
  {
    id: 'quote-contemporary-001',
    quote: 'The privilege of a lifetime is to become who you truly are.',
    author: 'Carl Jung',
    tradition: 'Contemporary',
    theme: 'Individuation and Authenticity',
    context: 'Jungian psychology on the process of becoming one\'s authentic self.',
    reflection: 'Our deepest work is discovering and expressing our authentic nature, beyond social conditioning and expectations.'
  },
  {
    id: 'quote-contemporary-002',
    quote: 'Between stimulus and response there is a space. In that space is our power to choose our response. In our response lies our growth and our freedom.',
    author: 'Viktor Frankl',
    tradition: 'Contemporary',
    theme: 'Choice and Freedom',
    context: 'From holocaust survivor and psychiatrist on human resilience and choice.',
    reflection: 'Even in the most difficult circumstances, we retain the power to choose our attitude and response.'
  }
]

// Helper functions
export const getQuotesByTradition = (tradition: string) =>
  philosophyQuotes.filter(quote => quote.tradition === tradition)

export const getQuotesByTheme = (theme: string) =>
  philosophyQuotes.filter(quote => quote.theme === theme)

export const getQuotesByAuthor = (author: string) =>
  philosophyQuotes.filter(quote => quote.author === author)

export const getRandomQuote = (tradition?: string) => {
  let filteredQuotes = philosophyQuotes
  
  if (tradition) {
    filteredQuotes = filteredQuotes.filter(quote => quote.tradition === tradition)
  }
  
  return filteredQuotes[Math.floor(Math.random() * filteredQuotes.length)]
}

export const getDailyQuote = () => {
  // Use date as seed for consistent daily quote
  const today = new Date().toDateString()
  const seed = today.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
  const index = seed % philosophyQuotes.length
  return philosophyQuotes[index]
}