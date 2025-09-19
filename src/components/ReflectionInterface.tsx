import { useState, useEffect } from 'react'
import { reflectionService, type ReflectionExercise, type ReflectionSession } from '../services/reflectionService'

interface ReflectionInterfaceProps {
  exerciseId: string
  onComplete: (session: ReflectionSession) => void
  onExit: () => void
}

const ReflectionInterface = ({ exerciseId, onComplete, onExit }: ReflectionInterfaceProps) => {
  const [exercise, setExercise] = useState<ReflectionExercise | null>(null)
  const [session, setSession] = useState<ReflectionSession | null>(null)
  const [currentStepIndex, setCurrentStepIndex] = useState(0)
  const [currentResponse, setCurrentResponse] = useState('')
  const [isTimerActive, setIsTimerActive] = useState(false)
  const [timeRemaining, setTimeRemaining] = useState(0)
  const [responses, setResponses] = useState<{ [stepId: string]: string }>({})

  useEffect(() => {
    const foundExercise = reflectionService.getExercisesByTradition('').find(ex => ex.id === exerciseId) ||
                          reflectionService.getExercisesByType('guided').find(ex => ex.id === exerciseId)
    
    if (foundExercise) {
      setExercise(foundExercise)
      const newSession = reflectionService.startReflectionSession(exerciseId)
      setSession(newSession)
    }
  }, [exerciseId])

  useEffect(() => {
    let interval: number | null = null
    
    if (isTimerActive && timeRemaining > 0) {
      interval = setInterval(() => {
        setTimeRemaining(time => {
          if (time <= 1) {
            setIsTimerActive(false)
            return 0
          }
          return time - 1
        })
      }, 1000)
    } else {
      setIsTimerActive(false)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [isTimerActive, timeRemaining])

  const startTimer = (seconds: number) => {
    setTimeRemaining(seconds)
    setIsTimerActive(true)
  }

  const handleNextStep = () => {
    if (!exercise || !session) return

    const currentStep = exercise.steps[currentStepIndex]
    
    // Save response if there's one
    if (currentResponse.trim() && (currentStep.type === 'question' || currentStep.type === 'writing')) {
      reflectionService.addResponse(session.id, currentStep.id, currentResponse)
      setResponses(prev => ({ ...prev, [currentStep.id]: currentResponse }))
      setCurrentResponse('')
    }

    if (currentStepIndex < exercise.steps.length - 1) {
      setCurrentStepIndex(prev => prev + 1)
      
      // Auto-start timer for next step if it has duration
      const nextStep = exercise.steps[currentStepIndex + 1]
      if (nextStep.duration) {
        startTimer(nextStep.duration)
      }
    } else {
      // Exercise complete
      handleComplete()
    }
  }

  const handlePrevStep = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex(prev => prev - 1)
      setIsTimerActive(false)
    }
  }

  const handleComplete = () => {
    if (!session) return

    // In a real app, you might show a completion modal to gather insights
    const insights = ['Completed reflection exercise']
    const nextSteps = ['Continue practicing mindful awareness']
    
    reflectionService.completeSession(session.id, insights, nextSteps, 'contemplative')
    const completedSession = reflectionService.getSession(session.id)
    
    if (completedSession) {
      onComplete(completedSession)
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
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

  if (!exercise || !session) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const currentStep = exercise.steps[currentStepIndex]
  const progress = ((currentStepIndex + 1) / exercise.steps.length) * 100

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className={`bg-gradient-to-r ${getTraditionColor(exercise.tradition)} text-white rounded-lg p-6 mb-6`}>
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-2xl font-bold mb-2">{exercise.title}</h1>
            <p className="opacity-90">{exercise.description}</p>
          </div>
          <button
            onClick={onExit}
            className="text-white hover:text-gray-200 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Progress Bar */}
        <div className="w-full bg-white bg-opacity-20 rounded-full h-2 mb-3">
          <div 
            className="bg-white rounded-full h-2 transition-all duration-300 ease-out"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        
        <div className="flex justify-between text-sm opacity-90">
          <span>{exercise.tradition} • {exercise.duration} min</span>
          <span>Step {currentStepIndex + 1} of {exercise.steps.length}</span>
        </div>
      </div>

      {/* Current Step */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
        {/* Timer */}
        {currentStep.duration && (
          <div className="flex items-center justify-between mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {isTimerActive ? 'Time Remaining' : 'Duration'}
            </span>
            <div className="flex items-center space-x-3">
              <span className={`text-lg font-mono ${isTimerActive ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400'}`}>
                {isTimerActive ? formatTime(timeRemaining) : formatTime(currentStep.duration)}
              </span>
              {!isTimerActive && currentStep.duration && (
                <button
                  onClick={() => startTimer(currentStep.duration!)}
                  className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition-colors"
                >
                  Start Timer
                </button>
              )}
            </div>
          </div>
        )}

        {/* Step Content */}
        <div className="mb-6">
          <div className="flex items-start mb-4">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium mr-4 flex-shrink-0 ${
              currentStep.type === 'question' ? 'bg-blue-500' :
              currentStep.type === 'instruction' ? 'bg-green-500' :
              currentStep.type === 'writing' ? 'bg-purple-500' :
              currentStep.type === 'contemplation' ? 'bg-indigo-500' :
              'bg-gray-500'
            }`}>
              {currentStep.type === 'question' ? '?' :
               currentStep.type === 'instruction' ? 'i' :
               currentStep.type === 'writing' ? '✍' :
               currentStep.type === 'contemplation' ? '◐' :
               '●'}
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                {currentStep.type.charAt(0).toUpperCase() + currentStep.type.slice(1)}
              </h3>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                {currentStep.content}
              </p>
            </div>
          </div>

          {/* Follow-up prompts */}
          {currentStep.followUp && (
            <div className="ml-12 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-2">Consider:</p>
              <ul className="text-sm text-blue-700 dark:text-blue-300 space-y-1">
                {currentStep.followUp.map((item, index) => (
                  <li key={index} className="flex items-start">
                    <span className="w-1 h-1 rounded-full bg-blue-400 mr-2 mt-2 flex-shrink-0"></span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Response Input */}
        {(currentStep.type === 'question' || currentStep.type === 'writing') && (
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Your Response
            </label>
            <textarea
              value={currentResponse}
              onChange={(e) => setCurrentResponse(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white resize-none"
              rows={4}
              placeholder="Take your time to reflect and write your thoughts..."
            />
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between">
          <button
            onClick={handlePrevStep}
            disabled={currentStepIndex === 0}
            className="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            ← Previous
          </button>

          <div className="space-x-3">
            {currentStepIndex < exercise.steps.length - 1 ? (
              <button
                onClick={handleNextStep}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
              >
                Next Step →
              </button>
            ) : (
              <button
                onClick={handleComplete}
                className="px-6 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
              >
                Complete Reflection
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Previous Responses Summary */}
      {Object.keys(responses).length > 0 && (
        <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-4">
          <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-3">Your Reflections So Far</h3>
          <div className="space-y-2 max-h-32 overflow-y-auto">
            {Object.entries(responses).map(([stepId, response], index) => (
              <div key={stepId} className="text-xs">
                <span className="font-medium text-gray-600 dark:text-gray-400">Step {index + 1}:</span>
                <span className="text-gray-700 dark:text-gray-300 ml-2">
                  {response.substring(0, 100)}...
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ReflectionInterface