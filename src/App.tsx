import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import ConversationSidebar from './components/ConversationSidebar'
import WisdomDashboard from './components/WisdomDashboard'
import { useConversationHistory } from './hooks/useConversationHistory'
import { type DailyWisdom } from './services/wisdomService'

type AppView = 'chat' | 'wisdom'

function App() {
  const [darkMode, setDarkMode] = useState(false)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [currentView, setCurrentView] = useState<AppView>('wisdom')
  const conversationHistory = useConversationHistory()

  const handleExportConversation = (conversationId: string) => {
    try {
      const exportData = conversationHistory.exportConversation(conversationId)
      const conversation = conversationHistory.conversations.find(c => c.id === conversationId)
      
      const blob = new Blob([exportData], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `philosophy-chat-${conversation?.title || 'conversation'}-${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Error exporting conversation:', error)
    }
  }

  const handleStartReflection = (wisdom: DailyWisdom) => {
    // Create a new conversation focused on reflection
    const reflectionTopic = `I'd like to reflect on today's wisdom from ${wisdom.quote.author}: "${wisdom.quote.quote}". Let's explore this together.`
    conversationHistory.createNewConversation()
    setCurrentView('chat')
    setSidebarOpen(false)
  }

  const handleStartConversation = (topic: string) => {
    // Start a conversation with the given topic
    conversationHistory.createNewConversation()
    setCurrentView('chat')
    setSidebarOpen(false)
    // The topic will be sent as the first message when ChatInterface loads
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'dark' : ''}`}>
      <div className="bg-white dark:bg-gray-900 transition-colors duration-300">
        {/* Header */}
        <header className="border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center space-x-4">
                {/* Mobile menu button - only show in chat view */}
                {currentView === 'chat' && (
                  <button
                    onClick={() => setSidebarOpen(!sidebarOpen)}
                    className="lg:hidden p-2 rounded-md text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                    </svg>
                  </button>
                )}

                <div>
                  <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                    Philosophy Chat
                  </h1>
                  <p className="text-sm text-gray-600 dark:text-gray-300">
                    Your AI companion for daily wisdom and reflection
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                {/* Navigation */}
                <nav className="hidden md:flex space-x-1">
                  <button
                    onClick={() => setCurrentView('wisdom')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      currentView === 'wisdom'
                        ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                    </svg>
                    Daily Wisdom
                  </button>
                  <button
                    onClick={() => setCurrentView('chat')}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                      currentView === 'chat'
                        ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                        : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`}
                  >
                    <svg className="w-4 h-4 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                    </svg>
                    Philosophy Chat
                  </button>
                </nav>
                
                {/* Theme Toggle */}
                <button
                  onClick={() => setDarkMode(!darkMode)}
                  className="p-2 rounded-lg bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                >
                  {darkMode ? (
                    <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                    </svg>
                  )}
                </button>
              </div>
            </div>

            {/* Mobile Navigation */}
            <nav className="md:hidden flex space-x-1 mt-4">
              <button
                onClick={() => setCurrentView('wisdom')}
                className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentView === 'wisdom'
                    ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                Daily Wisdom
              </button>
              <button
                onClick={() => setCurrentView('chat')}
                className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  currentView === 'chat'
                    ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                    : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                Philosophy Chat
              </button>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="h-[calc(100vh-129px)] md:h-[calc(100vh-73px)]">
          {currentView === 'wisdom' ? (
            /* Wisdom Dashboard */
            <div className="h-full overflow-y-auto">
              <div className="max-w-4xl mx-auto px-4 py-6">
                <WisdomDashboard
                  onStartReflection={handleStartReflection}
                  onStartConversation={handleStartConversation}
                />
              </div>
            </div>
          ) : (
            /* Chat View with Sidebar */
            <div className="flex h-full">
              <ConversationSidebar
                conversations={conversationHistory.conversations}
                currentConversation={conversationHistory.currentConversation}
                onSelectConversation={conversationHistory.switchToConversation}
                onNewConversation={() => {
                  conversationHistory.createNewConversation()
                  setSidebarOpen(false)
                }}
                onDeleteConversation={conversationHistory.deleteConversation}
                onExportConversation={handleExportConversation}
                isOpen={sidebarOpen}
                onToggle={() => setSidebarOpen(!sidebarOpen)}
              />

              <div className="flex-1 lg:pl-0">
                <ChatInterface conversationHistory={conversationHistory} />
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

export default App