import { useState, useEffect } from 'react'
import { wisdomService, type DailyWisdom } from '../services/wisdomService'

interface DailyWisdomProps {
  onStartReflection?: (wisdom: DailyWisdom) => void
  className?: string
}

const DailyWisdom = ({ onStartReflection, className = '' }: DailyWisdomProps) => {
  const [dailyWisdom, setDailyWisdom] = useState<DailyWisdom | null>(null)
  const [isExpanded, setIsExpanded] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadDailyWisdom = () => {
      try {
        const wisdom = wisdomService.getDailyWisdom()
        setDailyWisdom(wisdom)
      } catch (error) {
        console.error('Error loading daily wisdom:', error)
      } finally {
        setLoading(false)
      }
    }

    loadDailyWisdom()
  }, [])

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      weekday: 'long',
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

  const getTraditionColor = (tradition: string) => {
    const colors = {
      'Stoicism': 'from-blue-400 to-blue-600',
      'Buddhism': 'from-orange-400 to-orange-600',
      'Existentialism': 'from-purple-400 to-purple-600',
      'Ancient Greek': 'from-indigo-400 to-indigo-600',
      'Taoism': 'from-green-400 to-green-600',
      'Modern Philosophy': 'from-red-400 to-red-600',
      'Contemporary': 'from-gray-400 to-gray-600'
    }
    return colors[tradition as keyof typeof colors] || 'from-gray-400 to-gray-600'
  }

  if (loading) {
    return (
      <div className={`${className}`}>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded w-3/4 mb-4"></div>
            <div className="h-3 bg-gray-200 dark:bg-gray-600 rounded w-1/2 mb-2"></div>
            <div className="h-20 bg-gray-200 dark:bg-gray-600 rounded mb-4"></div>
          </div>
        </div>
      </div>
    )
  }

  if (!dailyWisdom) {
    return null
  }

  return (
    <div className={`${className}`}>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
        {/* Header with gradient */}
        <div className={`bg-gradient-to-r ${getTraditionColor(dailyWisdom.quote.tradition)} p-4 text-white`}>
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold">Daily Wisdom</h2>
              <p className="text-sm opacity-90">{formatDate(dailyWisdom.date)}</p>
            </div>
            <div className="text-right">
              <span className="text-xs bg-white bg-opacity-20 px-2 py-1 rounded-full">
                {dailyWisdom.quote.tradition}
              </span>
            </div>
          </div>
        </div>

        <div className="p-6">
          {/* Quote Section */}
          <div className="mb-6">
            <blockquote className="text-lg italic text-gray-700 dark:text-gray-300 mb-2">
              "{dailyWisdom.quote.quote}"
            </blockquote>
            <cite className="text-sm font-medium text-gray-900 dark:text-white">
              — {dailyWisdom.quote.author}
            </cite>
          </div>

          {/* Reflection */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-2 uppercase tracking-wide">
              Reflection
            </h3>
            <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
              {dailyWisdom.quote.reflection}
            </p>
          </div>

          {/* Practical Application */}
          <div className="mb-6">
            <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-2 uppercase tracking-wide">
              Today's Practice
            </h3>
            <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
                {dailyWisdom.practicalApplication}
              </p>
            </div>
          </div>

          {/* Expandable Section */}
          <div>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="flex items-center justify-between w-full text-left py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <span>Deeper Exploration</span>
              <svg
                className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>

            {isExpanded && (
              <div className="mt-4 space-y-4 border-t border-gray-200 dark:border-gray-600 pt-4">
                {/* Philosophical Prompt */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    Today's Philosophical Question
                  </h4>
                  <p className="text-gray-700 dark:text-gray-300 text-sm italic mb-2">
                    {dailyWisdom.prompt.content}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {dailyWisdom.prompt.context}
                  </p>
                </div>

                {/* Reflection Questions */}
                <div>
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-3">
                    Reflection Questions
                  </h4>
                  <ul className="space-y-2">
                    {dailyWisdom.reflectionQuestions.map((question, index) => (
                      <li key={index} className="flex items-start">
                        <span className="w-5 h-5 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-xs font-medium text-gray-600 dark:text-gray-400 mr-3 mt-0.5 flex-shrink-0">
                          {index + 1}
                        </span>
                        <span className="text-sm text-gray-700 dark:text-gray-300">
                          {question}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Action Buttons */}
                <div className="flex space-x-3 pt-4">
                  {onStartReflection && (
                    <button
                      onClick={() => onStartReflection(dailyWisdom)}
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors flex items-center justify-center"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                      Start Reflection
                    </button>
                  )}
                  
                  <button
                    onClick={() => {
                      const text = `Daily Wisdom - ${formatDate(dailyWisdom.date)}\n\n"${dailyWisdom.quote.quote}"\n— ${dailyWisdom.quote.author}\n\n${dailyWisdom.quote.reflection}`
                      navigator.clipboard.writeText(text)
                    }}
                    className="px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 text-sm font-medium rounded-lg transition-colors"
                  >
                    Share
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default DailyWisdom