import { useState } from 'react'
import MessageList from './MessageList'
import MessageInput from './MessageInput'

export interface Message {
  id: string
  content: string
  sender: 'user' | 'assistant'
  timestamp: Date
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Welcome to Philosophy Chat! I\'m here to explore the depths of wisdom with you. What philosophical question or topic would you like to discuss today?',
      sender: 'assistant',
      timestamp: new Date()
    }
  ])
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    // TODO: Integrate with OpenAI API
    // For now, simulate a response
    setTimeout(() => {
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `That's a fascinating question about "${content}". Let me reflect on this from a philosophical perspective...

From a Stoic viewpoint, we might consider how this relates to what is within our control versus what is not. The ancient philosopher Epictetus taught us that we cannot control external events, but we can control our responses to them.

What aspect of this topic resonates most with your current life experience?`,
        sender: 'assistant',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1500)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] bg-white dark:bg-gray-900">
      <MessageList messages={messages} isLoading={isLoading} />
      <MessageInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  )
}

export default ChatInterface