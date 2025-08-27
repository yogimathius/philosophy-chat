import { useState, useEffect } from 'react'
import DailyWisdom from './DailyWisdom'
import { wisdomService, type DailyWisdom as DailyWisdomType, type WisdomPreferences } from '../services/wisdomService'
import { getAllTraditions } from '../data/philosophyPrompts'

interface WisdomDashboardProps {
  onStartReflection: (wisdom: DailyWisdomType) => void
  onStartConversation: (topic: string) => void
}

const WisdomDashboard = ({ onStartReflection, onStartConversation }: WisdomDashboardProps) => {
  const [preferences, setPreferences] = useState<WisdomPreferences | null>(null)
  const [showPreferences, setShowPreferences] = useState(false)
  const [wisdomHistory, setWisdomHistory] = useState<DailyWisdomType[]>([])
  const [weeklyReflection, setWeeklyReflection] = useState<any>(null)

  const traditions = getAllTraditions()

  useEffect(() => {
    // Load preferences and history
    const prefs = wisdomService.getWisdomPreferences()
    setPreferences(prefs)
    
    const history = wisdomService.getWisdomHistory(7)
    setWisdomHistory(history)
    
    if (history.length >= 3) {
      const reflection = wisdomService.generateWeeklyReflection()
      setWeeklyReflection(reflection)
    }
  }, [])

  const handleUpdatePreferences = (newPrefs: WisdomPreferences) => {
    wisdomService.setWisdomPreferences(newPrefs)
    setPreferences(newPrefs)
    setShowPreferences(false)
  }

  const handleExploreTheme = (theme: string) => {
    const wisdom = wisdomService.getThemedWisdom(theme)
    onStartReflection(wisdom)
  }

  const quickTopics = [
    { name: 'Finding Purpose', theme: 'meaning', tradition: 'Existentialism' },
    { name: 'Dealing with Stress', theme: 'resilience', tradition: 'Stoicism' },
    { name: 'Mindful Living', theme: 'awareness', tradition: 'Buddhism' },
    { name: 'Authentic Self', theme: 'authenticity', tradition: 'Existentialism' },
    { name: 'Inner Peace', theme: 'tranquility', tradition: 'Taoism' },
    { name: 'Ethical Choices', theme: 'ethics', tradition: 'Ancient Greek' }
  ]

  if (!preferences) {
    return <div className="animate-pulse bg-gray-200 dark:bg-gray-700 rounded-lg h-96"></div>
  }

  return (
    <div className="space-y-6">
      {/* Header with Preferences */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Wisdom & Reflection
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Your daily journey of philosophical discovery
          </p>
        </div>
        
        <button
          onClick={() => setShowPreferences(true)}
          className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Preferences
        </button>
      </div>

      {/* Daily Wisdom Card */}
      <DailyWisdom onStartReflection={onStartReflection} />

      {/* Quick Exploration Topics */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Quick Philosophical Explorations
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {quickTopics.map((topic) => (
            <button
              key={topic.name}
              onClick={() => onStartConversation(`I'd like to explore ${topic.name.toLowerCase()} from a ${topic.tradition} perspective.`)}
              className="p-4 text-left bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors group"
            >
              <h3 className="font-medium text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                {topic.name}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                {topic.tradition} perspective
              </p>
            </button>
          ))}
        </div>
      </div>

      {/* Weekly Reflection Summary */}
      {weeklyReflection && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg p-6 border border-purple-200 dark:border-purple-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
            <svg className="w-5 h-5 mr-2 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            Weekly Insight
          </h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">Themes Explored</h3>
              <div className="flex flex-wrap gap-2">
                {weeklyReflection.themes.map((theme: string, index: number) => (
                  <span key={index} className="px-2 py-1 bg-purple-100 dark:bg-purple-800 text-purple-800 dark:text-purple-200 text-sm rounded-full">
                    {theme}
                  </span>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="font-medium text-gray-900 dark:text-white mb-2">Key Insights</h3>
              <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
                {weeklyReflection.insights.slice(0, 2).map((insight: string, index: number) => (
                  <li key={index} className="flex items-start">
                    <span className="w-1 h-1 rounded-full bg-purple-400 mr-2 mt-2 flex-shrink-0"></span>
                    {insight}
                  </li>
                ))}
              </ul>
            </div>

            <div className="pt-2 border-t border-purple-200 dark:border-purple-700">
              <p className="text-sm font-medium text-purple-900 dark:text-purple-100">
                {weeklyReflection.nextWeekFocus}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Wisdom History */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Recent Wisdom
        </h2>
        {wisdomHistory.length === 0 ? (
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            Your wisdom journey will appear here as you explore daily insights.
          </p>
        ) : (
          <div className="space-y-3">
            {wisdomHistory.slice(-5).reverse().map((wisdom) => (
              <div key={wisdom.id} className="flex items-start justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {wisdom.quote.author} • {wisdom.quote.tradition}
                  </p>
                  <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                    "{wisdom.quote.quote}"
                  </p>
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400 ml-3">
                  {new Date(wisdom.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Preferences Modal */}
      {showPreferences && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
              Wisdom Preferences
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Preferred Traditions
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {traditions.map((tradition) => (
                    <label key={tradition} className="flex items-center">
                      <input
                        type="checkbox"
                        checked={preferences.traditions.includes(tradition)}
                        onChange={(e) => {
                          const newTraditions = e.target.checked
                            ? [...preferences.traditions, tradition]
                            : preferences.traditions.filter(t => t !== tradition)
                          setPreferences({ ...preferences, traditions: newTraditions })
                        }}
                        className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        {tradition}
                      </span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Difficulty Level
                </label>
                <select
                  value={preferences.difficulty}
                  onChange={(e) => setPreferences({ ...preferences, difficulty: e.target.value as any })}
                  className="w-full px-3 py-2 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md text-gray-900 dark:text-white"
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
            </div>

            <div className="flex space-x-3 mt-6">
              <button
                onClick={() => handleUpdatePreferences(preferences)}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
              >
                Save
              </button>
              <button
                onClick={() => setShowPreferences(false)}
                className="flex-1 bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-300 font-medium py-2 px-4 rounded-lg transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default WisdomDashboard