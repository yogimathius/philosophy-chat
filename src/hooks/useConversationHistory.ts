import { useState, useEffect } from 'react'
import { Message } from '../components/ChatInterface'
import { ConversationContext } from '../services/openaiService'

export interface Conversation {
  id: string
  title: string
  messages: Message[]
  context: ConversationContext
  createdAt: Date
  updatedAt: Date
}

const STORAGE_KEY = 'philosophy-chat-conversations'
const CURRENT_CONVERSATION_KEY = 'philosophy-chat-current'

export const useConversationHistory = () => {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [currentConversation, setCurrentConversation] = useState<string | null>(null)

  // Load conversations from localStorage on mount
  useEffect(() => {
    const savedConversations = localStorage.getItem(STORAGE_KEY)
    const savedCurrentId = localStorage.getItem(CURRENT_CONVERSATION_KEY)
    
    if (savedConversations) {
      try {
        const parsed = JSON.parse(savedConversations)
        // Convert date strings back to Date objects
        const conversationsWithDates = parsed.map((conv: any) => ({
          ...conv,
          createdAt: new Date(conv.createdAt),
          updatedAt: new Date(conv.updatedAt),
          messages: conv.messages.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          }))
        }))
        setConversations(conversationsWithDates)
      } catch (error) {
        console.error('Error loading conversations:', error)
        localStorage.removeItem(STORAGE_KEY)
      }
    }

    if (savedCurrentId) {
      setCurrentConversation(savedCurrentId)
    }
  }, [])

  // Save conversations to localStorage whenever they change
  useEffect(() => {
    if (conversations.length > 0) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations))
    }
  }, [conversations])

  // Save current conversation ID
  useEffect(() => {
    if (currentConversation) {
      localStorage.setItem(CURRENT_CONVERSATION_KEY, currentConversation)
    }
  }, [currentConversation])

  const generateConversationTitle = (messages: Message[]): string => {
    if (messages.length === 0) return 'New Conversation'
    
    const firstUserMessage = messages.find(msg => msg.sender === 'user')
    if (firstUserMessage) {
      // Extract first few words for title
      const words = firstUserMessage.content.trim().split(' ').slice(0, 6)
      return words.length > 0 ? words.join(' ') + (firstUserMessage.content.split(' ').length > 6 ? '...' : '') : 'New Conversation'
    }
    
    return 'New Conversation'
  }

  const createNewConversation = (
    initialMessages: Message[] = [],
    context: ConversationContext = {}
  ): Conversation => {
    const newConversation: Conversation = {
      id: Date.now().toString(),
      title: generateConversationTitle(initialMessages),
      messages: initialMessages,
      context,
      createdAt: new Date(),
      updatedAt: new Date()
    }

    setConversations(prev => [newConversation, ...prev])
    setCurrentConversation(newConversation.id)
    return newConversation
  }

  const updateConversation = (
    conversationId: string,
    updates: Partial<Pick<Conversation, 'messages' | 'context' | 'title'>>
  ) => {
    setConversations(prev => prev.map(conv => {
      if (conv.id === conversationId) {
        const updatedConv = {
          ...conv,
          ...updates,
          updatedAt: new Date()
        }
        
        // Auto-update title if messages changed and title wasn't explicitly set
        if (updates.messages && !updates.title) {
          updatedConv.title = generateConversationTitle(updates.messages)
        }
        
        return updatedConv
      }
      return conv
    }))
  }

  const deleteConversation = (conversationId: string) => {
    setConversations(prev => prev.filter(conv => conv.id !== conversationId))
    
    if (currentConversation === conversationId) {
      const remainingConversations = conversations.filter(conv => conv.id !== conversationId)
      setCurrentConversation(remainingConversations.length > 0 ? remainingConversations[0].id : null)
    }
  }

  const switchToConversation = (conversationId: string) => {
    setCurrentConversation(conversationId)
  }

  const getCurrentConversation = (): Conversation | null => {
    if (!currentConversation) return null
    return conversations.find(conv => conv.id === currentConversation) || null
  }

  const searchConversations = (query: string): Conversation[] => {
    const lowercaseQuery = query.toLowerCase()
    return conversations.filter(conv => 
      conv.title.toLowerCase().includes(lowercaseQuery) ||
      conv.messages.some(msg => 
        msg.content.toLowerCase().includes(lowercaseQuery)
      )
    )
  }

  const getConversationsByTradition = (tradition: string): Conversation[] => {
    return conversations.filter(conv => conv.context.tradition === tradition)
  }

  const exportConversation = (conversationId: string): string => {
    const conversation = conversations.find(conv => conv.id === conversationId)
    if (!conversation) throw new Error('Conversation not found')

    const exportData = {
      title: conversation.title,
      createdAt: conversation.createdAt,
      tradition: conversation.context.tradition || 'General',
      difficulty: conversation.context.difficulty || 'beginner',
      messages: conversation.messages.map(msg => ({
        sender: msg.sender,
        content: msg.content,
        timestamp: msg.timestamp
      }))
    }

    return JSON.stringify(exportData, null, 2)
  }

  const clearAllConversations = () => {
    setConversations([])
    setCurrentConversation(null)
    localStorage.removeItem(STORAGE_KEY)
    localStorage.removeItem(CURRENT_CONVERSATION_KEY)
  }

  return {
    conversations,
    currentConversation,
    getCurrentConversation,
    createNewConversation,
    updateConversation,
    deleteConversation,
    switchToConversation,
    searchConversations,
    getConversationsByTradition,
    exportConversation,
    clearAllConversations
  }
}