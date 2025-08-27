import OpenAI from 'openai'
import { getRandomPrompt } from '../data/philosophyPrompts'
import { getRandomQuote } from '../data/philosophyQuotes'

// Initialize OpenAI client
const openai = new OpenAI({
  apiKey: import.meta.env.VITE_OPENAI_API_KEY,
  dangerouslyAllowBrowser: true // Only for demo - use backend in production
})

export interface ConversationContext {
  tradition?: string
  difficulty?: 'beginner' | 'intermediate' | 'advanced'
  theme?: string
  userPreferences?: {
    favoritePhilosophers?: string[]
    interests?: string[]
    learningStyle?: 'socratic' | 'explanatory' | 'contemplative'
  }
  conversationHistory?: Array<{
    role: 'user' | 'assistant'
    content: string
  }>
}

export class PhilosophyAIService {
  private systemPrompt = `You are a wise and compassionate philosophy companion, deeply knowledgeable in philosophical traditions from around the world. Your purpose is to engage users in meaningful philosophical conversations that promote wisdom, self-reflection, and personal growth.

Core Principles:
- Be genuinely curious about the user's thoughts and experiences
- Ask thoughtful follow-up questions that encourage deeper reflection
- Draw from diverse philosophical traditions (Stoicism, Buddhism, Existentialism, Ancient Greek, Taoism, etc.)
- Make complex philosophical concepts accessible without oversimplifying
- Encourage practical application of philosophical insights to daily life
- Maintain a warm, encouraging tone that invites exploration
- Respect the user's journey and avoid being preachy or dogmatic

Conversation Style:
- Use the Socratic method when appropriate - guide through questions rather than lecturing
- Share relevant quotes, examples, or stories from philosophical traditions
- Connect abstract concepts to concrete, relatable experiences
- Encourage the user to think critically and form their own insights
- Be comfortable with uncertainty and paradox - philosophy often embraces complexity

When discussing philosophical topics:
1. Start with the user's experience and perspective
2. Introduce relevant philosophical insights naturally
3. Ask questions that deepen understanding
4. Encourage practical reflection and application
5. Suggest connections to other philosophical ideas when relevant

Remember: You are a companion on the philosophical journey, not a teacher delivering lectures. Your goal is to facilitate the user's own discovery and understanding.`

  async generatePhilosophicalResponse(
    userMessage: string,
    context: ConversationContext = {}
  ): Promise<string> {
    try {
      const messages: Array<{ role: 'system' | 'user' | 'assistant'; content: string }> = [
        { role: 'system', content: this.createContextualSystemPrompt(context) }
      ]

      // Add conversation history if available
      if (context.conversationHistory) {
        messages.push(...context.conversationHistory)
      }

      // Add current user message
      messages.push({ role: 'user', content: userMessage })

      const completion = await openai.chat.completions.create({
        model: 'gpt-4',
        messages,
        temperature: 0.7,
        max_tokens: 800,
        presence_penalty: 0.1,
        frequency_penalty: 0.1
      })

      return completion.choices[0]?.message?.content || 'I apologize, but I\'m having trouble formulating a response right now. Could you try rephrasing your question?'
    } catch (error) {
      console.error('OpenAI API Error:', error)
      return this.getErrorResponse(error)
    }
  }

  private createContextualSystemPrompt(context: ConversationContext): string {
    let contextualPrompt = this.systemPrompt

    if (context.tradition) {
      contextualPrompt += `\n\nFocus: The user is particularly interested in ${context.tradition} philosophy. Draw primarily from this tradition while making connections to other philosophical schools when relevant.`
    }

    if (context.difficulty) {
      const difficultyGuides = {
        beginner: 'Keep explanations accessible and provide context for philosophical terms. Use everyday examples to illustrate concepts.',
        intermediate: 'You can use philosophical terminology with brief explanations. Encourage deeper analysis and critical thinking.',
        advanced: 'Engage with complex philosophical arguments and nuanced distinctions. Challenge the user with sophisticated questions.'
      }
      contextualPrompt += `\n\nDifficulty Level: ${difficultyGuides[context.difficulty]}`
    }

    if (context.theme) {
      contextualPrompt += `\n\nThematic Focus: The current conversation theme is ${context.theme}. Keep responses relevant to this theme while allowing natural conversation flow.`
    }

    if (context.userPreferences?.learningStyle) {
      const styleGuides = {
        socratic: 'Use primarily Socratic questioning - guide the user to insights through thoughtful questions rather than direct explanations.',
        explanatory: 'Provide clear explanations and context, then encourage reflection and application.',
        contemplative: 'Focus on deep reflection and personal meaning-making. Encourage quiet contemplation and inner wisdom.'
      }
      contextualPrompt += `\n\nLearning Style: ${styleGuides[context.userPreferences.learningStyle]}`
    }

    return contextualPrompt
  }

  private getErrorResponse(error: unknown): string {
    if (error instanceof Error) {
      if (error.message.includes('API key')) {
        return 'I need an OpenAI API key to provide philosophical insights. Please check your configuration and try again.'
      }
      if (error.message.includes('rate limit')) {
        return 'I\'m receiving too many requests right now. Let\'s take a moment to reflect on our previous conversation before continuing.'
      }
      if (error.message.includes('network')) {
        return 'I\'m having trouble connecting right now. While we wait, perhaps you could reflect on what we\'ve discussed so far?'
      }
    }
    
    return 'I\'m experiencing some technical difficulties. In the spirit of Stoicism, let\'s accept what we cannot control and focus on what we can - continuing our philosophical exploration together.'
  }

  async generatePhilosophicalPrompt(context: ConversationContext = {}): Promise<string> {
    const prompt = getRandomPrompt(context.tradition, context.difficulty)
    if (!prompt) return "What philosophical question has been on your mind lately?"

    const contextualIntro = `Here's a thoughtful question from ${prompt.tradition}${prompt.author ? ` (inspired by ${prompt.author})` : ''}:

"${prompt.content}"

${prompt.context}

${prompt.followUpQuestions.length > 0 ? '\nSome questions to consider:\n' + prompt.followUpQuestions.map(q => `• ${q}`).join('\n') : ''}

What are your initial thoughts on this?`

    return contextualIntro
  }

  async generateDailyWisdom(): Promise<string> {
    const quote = getRandomQuote()
    if (!quote) return "Today is a good day for philosophical reflection."

    return `**Daily Wisdom from ${quote.author}** (${quote.tradition})

"${quote.quote}"

**Context:** ${quote.context}

**Reflection:** ${quote.reflection}

How does this wisdom speak to your current life situation?`
  }
}

export const philosophyAI = new PhilosophyAIService()