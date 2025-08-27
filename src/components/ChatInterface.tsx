import { useState, useEffect } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import PhilosophySelector from './PhilosophySelector'
import { philosophyAI, type ConversationContext } from '../services/openaiService'
import { getDailyQuote } from '../data/philosophyQuotes'

export interface Message {
  id: string
  content: string
  sender: 'user' | 'assistant'
  timestamp: Date
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [context, setContext] = useState<ConversationContext>({
    difficulty: 'beginner',
    userPreferences: {
      learningStyle: 'explanatory'
    }
  })

  // Initialize with daily wisdom
  useEffect(() => {
    const initializeChat = async () => {
      try {
        const dailyWisdom = await philosophyAI.generateDailyWisdom()
        const welcomeMessage: Message = {
          id: '1',
          content: `Welcome to Philosophy Chat! I'm here to explore the depths of wisdom with you. 

${dailyWisdom}

What would you like to explore today?`,
          sender: 'assistant',
          timestamp: new Date()
        }
        setMessages([welcomeMessage])
      } catch (error) {
        // Fallback welcome message
        const fallbackQuote = getDailyQuote()
        const welcomeMessage: Message = {
          id: '1',
          content: `Welcome to Philosophy Chat! I'm here to explore the depths of wisdom with you.

**Daily Wisdom from ${fallbackQuote.author}** (${fallbackQuote.tradition})

"${fallbackQuote.quote}"

**Reflection:** ${fallbackQuote.reflection}

What philosophical question or topic would you like to discuss today?`,
          sender: 'assistant',
          timestamp: new Date()
        }
        setMessages([welcomeMessage])
      }
    }

    initializeChat()
  }, [])

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Build conversation history for context
      const conversationHistory = messages.slice(-6).map(msg => ({
        role: msg.sender === 'user' ? 'user' as const : 'assistant' as const,
        content: msg.content
      }))

      const updatedContext: ConversationContext = {
        ...context,
        conversationHistory
      }

      const response = await philosophyAI.generatePhilosophicalResponse(content, updatedContext)
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        sender: 'assistant',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error generating response:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'I\'m experiencing some technical difficulties right now. In the meantime, perhaps you could reflect on what philosophical insights have been most meaningful to you recently?',
        sender: 'assistant',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleContextChange = (newContext: ConversationContext) => {
    setContext(newContext)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-white dark:bg-gray-900">
      <PhilosophySelector context={context} onContextChange={handleContextChange} />
      <MessageList messages={messages} isLoading={isLoading} />
      <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  )
}

export default ChatInterface