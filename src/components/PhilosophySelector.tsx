import { useState } from 'react'
import { getAllTraditions } from '../data/philosophyPrompts'
import { type ConversationContext } from '../services/openaiService'

interface PhilosophySelectorProps {
  context: ConversationContext
  onContextChange: (context: ConversationContext) => void
}

const PhilosophySelector = ({ context, onContextChange }: PhilosophySelectorProps) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const traditions = getAllTraditions()

  const updateContext = (updates: Partial<ConversationContext>) => {
    onContextChange({ ...context, ...updates })
  }

  return (
    <div className="border-b border-gray-200 dark:border-gray-700">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-4 py-3 flex items-center justify-between text-left text-sm text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
      >
        <span>
          Philosophy Settings 
          {context.tradition && (
            <span className="ml-2 px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded">
              {context.tradition}
            </span>
          )}
          {context.difficulty && (
            <span className="ml-2 px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs rounded">
              {context.difficulty}
            </span>
          )}
        </span>
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
        <div className="px-4 pb-4 space-y-4 bg-gray-50 dark:bg-gray-800">
          {/* Tradition Selector */}
          <div>
            <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
              Philosophical Tradition
            </label>
            <select
              value={context.tradition || ''}
              onChange={(e) => updateContext({ tradition: e.target.value || undefined })}
              className="w-full px-3 py-2 text-sm bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 dark:text-white"
            >
              <option value="">All Traditions</option>
              {traditions.map((tradition) => (
                <option key={tradition} value={tradition}>
                  {tradition}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty Level */}
          <div>
            <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
              Difficulty Level
            </label>
            <div className="flex space-x-2">
              {['beginner', 'intermediate', 'advanced'].map((level) => (
                <button
                  key={level}
                  onClick={() => updateContext({ difficulty: level as any })}
                  className={`flex-1 px-3 py-2 text-xs rounded-md transition-colors ${
                    context.difficulty === level
                      ? 'bg-blue-600 text-white'
                      : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600'
                  }`}
                >
                  {level.charAt(0).toUpperCase() + level.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Learning Style */}
          <div>
            <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
              Learning Style
            </label>
            <div className="grid grid-cols-3 gap-2">
              {[
                { key: 'socratic', label: 'Socratic', desc: 'Questions & discovery' },
                { key: 'explanatory', label: 'Explanatory', desc: 'Clear explanations' },
                { key: 'contemplative', label: 'Contemplative', desc: 'Deep reflection' }
              ].map(({ key, label, desc }) => (
                <button
                  key={key}
                  onClick={() => updateContext({
                    userPreferences: {
                      ...context.userPreferences,
                      learningStyle: key as any
                    }
                  })}
                  className={`p-3 text-xs rounded-md transition-colors ${
                    context.userPreferences?.learningStyle === key
                      ? 'bg-green-600 text-white'
                      : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600'
                  }`}
                >
                  <div className="font-medium">{label}</div>
                  <div className="text-gray-500 dark:text-gray-400 text-xs mt-1">{desc}</div>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default PhilosophySelector