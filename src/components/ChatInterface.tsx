import { useState, useEffect } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'
import PhilosophySelector from './PhilosophySelector'
import { philosophyAI, type ConversationContext } from '../services/openaiService'
import { getDailyQuote } from '../data/philosophyQuotes'
import type { useConversationHistory } from '../hooks/useConversationHistory'

export interface Message {
  id: string
  content: string
  sender: 'user' | 'assistant'
  timestamp: Date
}

interface ChatInterfaceProps {
  conversationHistory: ReturnType<typeof useConversationHistory>
}

const ChatInterface = ({ conversationHistory }: ChatInterfaceProps) => {
  const [isLoading, setIsLoading] = useState(false)
  const [context, setContext] = useState<ConversationContext>({
    difficulty: 'beginner',
    userPreferences: {
      learningStyle: 'explanatory'
    }
  })

  const currentConversation = conversationHistory.getCurrentConversation()
  const messages = currentConversation?.messages || []

  // Initialize conversation if none exists
  useEffect(() => {
    if (!currentConversation) {
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
          
          conversationHistory.createNewConversation([welcomeMessage], context)
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
          
          conversationHistory.createNewConversation([welcomeMessage], context)
        }
      }

      initializeChat()
    }
  }, [currentConversation, context, conversationHistory])

  // Load context from current conversation
  useEffect(() => {
    if (currentConversation?.context) {
      setContext(currentConversation.context)
    }
  }, [currentConversation])

  const handleSendMessage = async (content: string) => {
    if (!currentConversation) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date()
    }

    const newMessages = [...messages, userMessage]
    conversationHistory.updateConversation(currentConversation.id, { 
      messages: newMessages,
      context
    })
    
    setIsLoading(true)

    try {
      // Build conversation history for context
      const recentHistory = messages.slice(-6).map(msg => ({
        role: msg.sender === 'user' ? 'user' as const : 'assistant' as const,
        content: msg.content
      }))

      const updatedContext: ConversationContext = {
        ...context,
        conversationHistory: recentHistory
      }

      const response = await philosophyAI.generatePhilosophicalResponse(content, updatedContext)
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response,
        sender: 'assistant',
        timestamp: new Date()
      }
      
      const finalMessages = [...newMessages, assistantMessage]
      conversationHistory.updateConversation(currentConversation.id, { 
        messages: finalMessages,
        context: updatedContext
      })
    } catch (error) {
      console.error('Error generating response:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'I\'m experiencing some technical difficulties right now. In the meantime, perhaps you could reflect on what philosophical insights have been most meaningful to you recently?',
        sender: 'assistant',
        timestamp: new Date()
      }
      
      const finalMessages = [...newMessages, errorMessage]
      conversationHistory.updateConversation(currentConversation.id, { 
        messages: finalMessages
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleContextChange = (newContext: ConversationContext) => {
    setContext(newContext)
    
    // Update the current conversation's context
    if (currentConversation) {
      conversationHistory.updateConversation(currentConversation.id, { 
        context: newContext 
      })
    }
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