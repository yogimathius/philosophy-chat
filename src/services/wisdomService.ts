import { getRandomQuote, getDailyQuote, type PhilosophyQuote } from '../data/philosophyQuotes'
import { getRandomPrompt, type PhilosophyPrompt } from '../data/philosophyPrompts'

export interface DailyWisdom {
  id: string
  date: string
  quote: PhilosophyQuote
  prompt: PhilosophyPrompt
  reflectionQuestions: string[]
  practicalApplication: string
  type: 'daily' | 'themed' | 'personal'
}

export interface WisdomPreferences {
  traditions: string[]
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  themes: string[]
  frequency: 'daily' | 'weekly' | 'custom'
  reminderTime?: string
}

export class WisdomService {
  private readonly WISDOM_STORAGE_KEY = 'philosophy-chat-wisdom'
  private readonly PREFERENCES_KEY = 'philosophy-chat-wisdom-preferences'

  getDailyWisdom(date?: Date): DailyWisdom {
    const targetDate = date || new Date()
    const dateString = targetDate.toISOString().split('T')[0]
    
    // Check if we already generated wisdom for this date
    const existingWisdom = this.getStoredWisdom(dateString)
    if (existingWisdom) {
      return existingWisdom
    }

    const preferences = this.getWisdomPreferences()
    
    // Get daily quote (consistent for the day)
    const quote = getDailyQuote()
    
    // Get prompt based on preferences or random
    const prompt = this.getContextualPrompt(preferences, targetDate)
    
    // Generate reflection questions
    const reflectionQuestions = this.generateReflectionQuestions(quote, prompt)
    
    // Create practical application
    const practicalApplication = this.generatePracticalApplication(quote, prompt)
    
    const dailyWisdom: DailyWisdom = {
      id: `daily-${dateString}`,
      date: dateString,
      quote,
      prompt,
      reflectionQuestions,
      practicalApplication,
      type: 'daily'
    }

    // Store for consistency
    this.storeWisdom(dailyWisdom)
    
    return dailyWisdom
  }

  getThemedWisdom(theme: string, tradition?: string): DailyWisdom {
    const dateString = new Date().toISOString().split('T')[0]
    
    // Get themed content
    const quote = getRandomQuote(tradition)
    const prompt = getRandomPrompt(tradition)
    
    if (!quote || !prompt) {
      // Fallback to daily wisdom
      return this.getDailyWisdom()
    }

    const reflectionQuestions = this.generateReflectionQuestions(quote, prompt, theme)
    const practicalApplication = this.generatePracticalApplication(quote, prompt, theme)
    
    return {
      id: `themed-${theme}-${dateString}`,
      date: dateString,
      quote,
      prompt,
      reflectionQuestions,
      practicalApplication,
      type: 'themed'
    }
  }

  private getContextualPrompt(preferences: WisdomPreferences, date: Date): PhilosophyPrompt {
    // Use date as seed for consistent daily selection
    const seed = date.getDate() + date.getMonth() * 31 + date.getFullYear() * 365
    
    let tradition: string | undefined
    if (preferences.traditions.length > 0) {
      tradition = preferences.traditions[seed % preferences.traditions.length]
    }

    const prompt = getRandomPrompt(tradition, preferences.difficulty)
    
    // Fallback if no prompt found with preferences
    return prompt || getRandomPrompt()!
  }

  private generateReflectionQuestions(
    quote: PhilosophyQuote, 
    prompt: PhilosophyPrompt, 
    theme?: string
  ): string[] {
    const baseQuestions = prompt.followUpQuestions || []
    
    const contextualQuestions = [
      `How does ${quote.author}'s insight "${quote.quote}" relate to your current life situation?`,
      `What would it look like to apply this wisdom in a specific challenge you're facing?`,
      `How might this perspective change your approach to difficult decisions?`
    ]

    if (theme) {
      contextualQuestions.push(
        `How does this wisdom specifically apply to the theme of ${theme}?`
      )
    }

    // Combine and take best mix
    const allQuestions = [...baseQuestions, ...contextualQuestions]
    return allQuestions.slice(0, 4) // Limit to 4 questions max
  }

  private generatePracticalApplication(
    quote: PhilosophyQuote, 
    prompt: PhilosophyPrompt,
    theme?: string
  ): string {
    const applications = [
      `Today, try applying ${quote.author}'s wisdom by pausing before reacting to any challenging situation and asking: "What would ${quote.author} do here?"`,
      
      `Practice the principle of ${prompt.theme.toLowerCase()} by identifying one area where you can apply this wisdom immediately.`,
      
      `Set an intention to notice moments throughout your day where you can embody the spirit of: "${quote.quote}"`,
      
      `Choose one relationship or responsibility where you can practice this philosophical approach today.`,
      
      `Create a simple daily ritual that reminds you of this wisdom - perhaps a morning reflection or evening review.`
    ]

    const seed = new Date().getDate() + quote.id.length + prompt.id.length
    return applications[seed % applications.length]
  }

  getWisdomPreferences(): WisdomPreferences {
    const stored = localStorage.getItem(this.PREFERENCES_KEY)
    if (stored) {
      try {
        return JSON.parse(stored)
      } catch (error) {
        console.error('Error parsing wisdom preferences:', error)
      }
    }

    // Default preferences
    return {
      traditions: [],
      difficulty: 'beginner',
      themes: [],
      frequency: 'daily'
    }
  }

  setWisdomPreferences(preferences: WisdomPreferences): void {
    localStorage.setItem(this.PREFERENCES_KEY, JSON.stringify(preferences))
  }

  private getStoredWisdom(date: string): DailyWisdom | null {
    const stored = localStorage.getItem(`${this.WISDOM_STORAGE_KEY}-${date}`)
    if (stored) {
      try {
        return JSON.parse(stored)
      } catch (error) {
        console.error('Error parsing stored wisdom:', error)
      }
    }
    return null
  }

  private storeWisdom(wisdom: DailyWisdom): void {
    localStorage.setItem(`${this.WISDOM_STORAGE_KEY}-${wisdom.date}`, JSON.stringify(wisdom))
  }

  getWisdomHistory(days: number = 7): DailyWisdom[] {
    const history: DailyWisdom[] = []
    const today = new Date()
    
    for (let i = 0; i < days; i++) {
      const date = new Date(today)
      date.setDate(today.getDate() - i)
      const dateString = date.toISOString().split('T')[0]
      
      const wisdom = this.getStoredWisdom(dateString)
      if (wisdom) {
        history.push(wisdom)
      }
    }
    
    return history.reverse() // Oldest first
  }

  clearWisdomHistory(): void {
    const keys = Object.keys(localStorage).filter(key => 
      key.startsWith(this.WISDOM_STORAGE_KEY)
    )
    keys.forEach(key => localStorage.removeItem(key))
  }

  generateWeeklyReflection(): {
    themes: string[]
    insights: string[]
    growth: string[]
    nextWeekFocus: string
  } {
    const weekWisdom = this.getWisdomHistory(7)
    
    const themes = [...new Set(weekWisdom.map(w => w.prompt.theme))]
    const insights = weekWisdom.map(w => `${w.quote.author}: "${w.quote.quote}"`).slice(0, 3)
    const growth = [
      'What patterns do you notice in your philosophical journey this week?',
      'Which wisdom resonated most deeply with your current life situation?',
      'How has your perspective shifted through these daily reflections?'
    ]
    
    const nextWeekFocus = themes.length > 0 
      ? `Consider exploring ${themes[Math.floor(Math.random() * themes.length)]} more deeply next week.`
      : 'Focus on applying one key insight consistently in your daily life.'

    return {
      themes,
      insights,
      growth,
      nextWeekFocus
    }
  }
}

export const wisdomService = new WisdomService()