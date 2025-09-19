export interface ReflectionExercise {
  id: string
  title: string
  description: string
  type: 'guided' | 'journaling' | 'contemplation' | 'socratic' | 'meditation'
  tradition: string
  duration: number // in minutes
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  steps: ReflectionStep[]
  themes: string[]
}

export interface ReflectionStep {
  id: string
  type: 'question' | 'instruction' | 'pause' | 'writing' | 'contemplation'
  content: string
  duration?: number // in seconds
  followUp?: string[]
}

export interface ReflectionResponse {
  exerciseId: string
  stepId: string
  response: string
  timestamp: Date
  completionTime?: number // in seconds
}

export interface ReflectionSession {
  id: string
  exerciseId: string
  startTime: Date
  endTime?: Date
  responses: ReflectionResponse[]
  insights: string[]
  nextSteps: string[]
  mood?: 'curious' | 'contemplative' | 'challenged' | 'peaceful' | 'confused' | 'inspired'
  completed: boolean
}

export const reflectionExercises: ReflectionExercise[] = [
  // Stoic Exercises
  {
    id: 'stoic-morning-reflection',
    title: 'Morning Stoic Reflection',
    description: 'Start your day with clarity about what you can and cannot control',
    type: 'guided',
    tradition: 'Stoicism',
    duration: 10,
    difficulty: 'beginner',
    themes: ['control', 'preparation', 'virtue'],
    steps: [
      {
        id: 'step-1',
        type: 'instruction',
        content: 'Find a quiet moment as you begin your day. Take three deep breaths and center yourself.',
        duration: 30
      },
      {
        id: 'step-2',
        type: 'question',
        content: 'What challenges or situations might I face today?',
        followUp: ['Be specific and honest about potential difficulties']
      },
      {
        id: 'step-3',
        type: 'writing',
        content: 'For each challenge you identified, write down: What aspects are within my control? What aspects are not?'
      },
      {
        id: 'step-4',
        type: 'question',
        content: 'How can I respond with virtue (wisdom, justice, courage, temperance) to today\'s challenges?'
      },
      {
        id: 'step-5',
        type: 'contemplation',
        content: 'Set an intention to focus your energy only on what is within your control today.',
        duration: 60
      }
    ]
  },

  {
    id: 'stoic-evening-review',
    title: 'Evening Stoic Review',
    description: 'Reflect on your day with wisdom and self-compassion',
    type: 'journaling',
    tradition: 'Stoicism',
    duration: 15,
    difficulty: 'intermediate',
    themes: ['reflection', 'growth', 'virtue'],
    steps: [
      {
        id: 'step-1',
        type: 'pause',
        content: 'Settle into a comfortable position and let the day settle in your mind.',
        duration: 30
      },
      {
        id: 'step-2',
        type: 'question',
        content: 'What went well today? How did I demonstrate virtue in my actions?'
      },
      {
        id: 'step-3',
        type: 'question',
        content: 'Where did I react from emotion rather than reason? What can I learn from this?',
        followUp: ['Be gentle with yourself - this is about learning, not judgment']
      },
      {
        id: 'step-4',
        type: 'writing',
        content: 'Write about one situation where you could have responded more wisely. How would a sage have handled it?'
      },
      {
        id: 'step-5',
        type: 'question',
        content: 'What am I grateful for from today? What did I learn about myself?'
      },
      {
        id: 'step-6',
        type: 'instruction',
        content: 'End with gratitude for the opportunity to practice wisdom and grow.',
        duration: 30
      }
    ]
  },

  // Buddhist Exercises
  {
    id: 'mindfulness-body-scan',
    title: 'Mindful Awareness Practice',
    description: 'Cultivate present-moment awareness through mindful observation',
    type: 'meditation',
    tradition: 'Buddhism',
    duration: 20,
    difficulty: 'beginner',
    themes: ['mindfulness', 'awareness', 'presence'],
    steps: [
      {
        id: 'step-1',
        type: 'instruction',
        content: 'Sit comfortably with your spine straight but not rigid. Close your eyes or soften your gaze.',
        duration: 30
      },
      {
        id: 'step-2',
        type: 'instruction',
        content: 'Begin by noticing your breath. Don\'t change it, just observe the natural rhythm.',
        duration: 120
      },
      {
        id: 'step-3',
        type: 'instruction',
        content: 'Now expand your awareness to include physical sensations throughout your body.',
        duration: 300
      },
      {
        id: 'step-4',
        type: 'instruction',
        content: 'Notice any thoughts that arise. Acknowledge them gently and return attention to the present moment.',
        duration: 300
      },
      {
        id: 'step-5',
        type: 'question',
        content: 'What did you notice about the quality of your attention? How did thoughts and sensations change?'
      },
      {
        id: 'step-6',
        type: 'contemplation',
        content: 'Rest in the awareness that observed all these experiences. This awareness is always available to you.',
        duration: 60
      }
    ]
  },

  {
    id: 'loving-kindness-meditation',
    title: 'Loving-Kindness Reflection',
    description: 'Cultivate compassion for yourself and others',
    type: 'meditation',
    tradition: 'Buddhism',
    duration: 15,
    difficulty: 'intermediate',
    themes: ['compassion', 'kindness', 'connection'],
    steps: [
      {
        id: 'step-1',
        type: 'instruction',
        content: 'Sit quietly and bring to mind your own image. Notice any feelings that arise.',
        duration: 30
      },
      {
        id: 'step-2',
        type: 'instruction',
        content: 'Silently repeat: "May I be happy. May I be healthy. May I be at peace. May I be free from suffering."',
        duration: 180
      },
      {
        id: 'step-3',
        type: 'instruction',
        content: 'Now bring to mind someone you care about. Extend the same wishes to them.',
        duration: 180
      },
      {
        id: 'step-4',
        type: 'instruction',
        content: 'Think of someone neutral - perhaps a cashier or neighbor. Offer them the same kind wishes.',
        duration: 180
      },
      {
        id: 'step-5',
        type: 'instruction',
        content: 'If you feel ready, bring to mind someone challenging and extend compassion to them too.',
        duration: 180
      },
      {
        id: 'step-6',
        type: 'question',
        content: 'How did it feel to extend kindness in different directions? What did you notice about resistance or ease?'
      }
    ]
  },

  // Socratic Exercises
  {
    id: 'socratic-self-inquiry',
    title: 'Socratic Self-Inquiry',
    description: 'Question your assumptions and beliefs through systematic inquiry',
    type: 'socratic',
    tradition: 'Ancient Greek',
    duration: 25,
    difficulty: 'advanced',
    themes: ['knowledge', 'assumptions', 'wisdom'],
    steps: [
      {
        id: 'step-1',
        type: 'question',
        content: 'Choose a belief or opinion you hold strongly. What is this belief?',
        followUp: ['Write it down clearly and specifically']
      },
      {
        id: 'step-2',
        type: 'question',
        content: 'How do I know this is true? What evidence supports this belief?'
      },
      {
        id: 'step-3',
        type: 'question',
        content: 'What assumptions am I making? What am I taking for granted?',
        followUp: ['Look for hidden assumptions you haven\'t questioned']
      },
      {
        id: 'step-4',
        type: 'question',
        content: 'What would someone who disagrees with me say? What is their strongest argument?'
      },
      {
        id: 'step-5',
        type: 'question',
        content: 'What are the implications if I\'m wrong about this? What would change?'
      },
      {
        id: 'step-6',
        type: 'writing',
        content: 'Write a brief reflection on what you\'ve discovered. Has your certainty about this belief changed?'
      },
      {
        id: 'step-7',
        type: 'contemplation',
        content: 'Rest in the space of "not knowing." What does intellectual humility feel like?',
        duration: 120
      }
    ]
  },

  // Existentialist Exercises
  {
    id: 'authentic-choice-reflection',
    title: 'Authentic Choice Reflection',
    description: 'Explore your freedom and responsibility in making authentic choices',
    type: 'journaling',
    tradition: 'Existentialism',
    duration: 20,
    difficulty: 'intermediate',
    themes: ['authenticity', 'freedom', 'responsibility'],
    steps: [
      {
        id: 'step-1',
        type: 'question',
        content: 'Think of a decision you need to make. What choice are you facing?'
      },
      {
        id: 'step-2',
        type: 'question',
        content: 'What would others expect you to choose? Family, friends, society?',
        followUp: ['Be honest about external pressures and expectations']
      },
      {
        id: 'step-3',
        type: 'question',
        content: 'What would you choose if no one else\'s opinion mattered? What feels most authentic to you?'
      },
      {
        id: 'step-4',
        type: 'writing',
        content: 'Write about the difference between these two choices. What does this reveal about external vs. internal motivation?'
      },
      {
        id: 'step-5',
        type: 'question',
        content: 'What are you afraid of if you choose authentically? What might you lose or gain?'
      },
      {
        id: 'step-6',
        type: 'contemplation',
        content: 'Reflect on your radical freedom to choose. How does it feel to be completely responsible for your choices?',
        duration: 180
      },
      {
        id: 'step-7',
        type: 'question',
        content: 'What would it look like to choose courageously and authentically in this situation?'
      }
    ]
  },

  // Taoist Exercises
  {
    id: 'wu-wei-reflection',
    title: 'Wu Wei (Effortless Action) Practice',
    description: 'Learn to align with natural flow rather than forcing outcomes',
    type: 'contemplation',
    tradition: 'Taoism',
    duration: 15,
    difficulty: 'beginner',
    themes: ['flow', 'naturalness', 'non-forcing'],
    steps: [
      {
        id: 'step-1',
        type: 'question',
        content: 'Think of an area in your life where you\'ve been pushing hard or forcing outcomes. What situation comes to mind?'
      },
      {
        id: 'step-2',
        type: 'question',
        content: 'What would it look like to approach this situation more like water flowing around obstacles?',
        followUp: ['Consider flexibility, patience, finding natural openings']
      },
      {
        id: 'step-3',
        type: 'instruction',
        content: 'Spend a few minutes observing your breath. Notice how it flows naturally without your control.',
        duration: 180
      },
      {
        id: 'step-4',
        type: 'question',
        content: 'How can you trust the natural timing and flow of your situation more?'
      },
      {
        id: 'step-5',
        type: 'writing',
        content: 'Write about what "effortless effort" might mean in your specific circumstances.'
      },
      {
        id: 'step-6',
        type: 'contemplation',
        content: 'Set an intention to notice opportunities for wu wei - acting in harmony with natural flow.',
        duration: 60
      }
    ]
  }
]

export class ReflectionService {
  private readonly SESSIONS_KEY = 'philosophy-chat-reflection-sessions'

  getExercisesByTradition(tradition: string): ReflectionExercise[] {
    return reflectionExercises.filter(exercise => exercise.tradition === tradition)
  }

  getExercisesByType(type: ReflectionExercise['type']): ReflectionExercise[] {
    return reflectionExercises.filter(exercise => exercise.type === type)
  }

  getExercisesByDifficulty(difficulty: ReflectionExercise['difficulty']): ReflectionExercise[] {
    return reflectionExercises.filter(exercise => exercise.difficulty === difficulty)
  }

  getRandomExercise(
    tradition?: string,
    difficulty?: ReflectionExercise['difficulty'],
    maxDuration?: number
  ): ReflectionExercise | null {
    let filteredExercises = reflectionExercises

    if (tradition) {
      filteredExercises = filteredExercises.filter(ex => ex.tradition === tradition)
    }

    if (difficulty) {
      filteredExercises = filteredExercises.filter(ex => ex.difficulty === difficulty)
    }

    if (maxDuration) {
      filteredExercises = filteredExercises.filter(ex => ex.duration <= maxDuration)
    }

    if (filteredExercises.length === 0) return null

    return filteredExercises[Math.floor(Math.random() * filteredExercises.length)]
  }

  startReflectionSession(exerciseId: string): ReflectionSession {
    const session: ReflectionSession = {
      id: Date.now().toString(),
      exerciseId,
      startTime: new Date(),
      responses: [],
      insights: [],
      nextSteps: [],
      completed: false
    }

    this.saveSession(session)
    return session
  }

  updateSession(sessionId: string, updates: Partial<ReflectionSession>): void {
    const sessions = this.getAllSessions()
    const sessionIndex = sessions.findIndex(s => s.id === sessionId)
    
    if (sessionIndex !== -1) {
      sessions[sessionIndex] = { ...sessions[sessionIndex], ...updates }
      this.saveSessions(sessions)
    }
  }

  addResponse(sessionId: string, stepId: string, response: string): void {
    const sessions = this.getAllSessions()
    const session = sessions.find(s => s.id === sessionId)
    
    if (session) {
      const reflectionResponse: ReflectionResponse = {
        exerciseId: session.exerciseId,
        stepId,
        response,
        timestamp: new Date()
      }
      
      session.responses.push(reflectionResponse)
      this.saveSessions(sessions)
    }
  }

  completeSession(sessionId: string, insights: string[], nextSteps: string[], mood?: ReflectionSession['mood']): void {
    this.updateSession(sessionId, {
      endTime: new Date(),
      insights,
      nextSteps,
      mood,
      completed: true
    })
  }

  getSession(sessionId: string): ReflectionSession | null {
    const sessions = this.getAllSessions()
    return sessions.find(s => s.id === sessionId) || null
  }

  getAllSessions(): ReflectionSession[] {
    const stored = localStorage.getItem(this.SESSIONS_KEY)
    if (stored) {
      try {
        const sessions = JSON.parse(stored)
        return sessions.map((session: any) => ({
          ...session,
          startTime: new Date(session.startTime),
          endTime: session.endTime ? new Date(session.endTime) : undefined,
          responses: session.responses.map((response: any) => ({
            ...response,
            timestamp: new Date(response.timestamp)
          }))
        }))
      } catch (error) {
        console.error('Error parsing reflection sessions:', error)
        return []
      }
    }
    return []
  }

  getRecentSessions(limit: number = 10): ReflectionSession[] {
    return this.getAllSessions()
      .sort((a, b) => b.startTime.getTime() - a.startTime.getTime())
      .slice(0, limit)
  }

  getSessionsByTradition(tradition: string): ReflectionSession[] {
    return this.getAllSessions().filter(session => {
      const exercise = reflectionExercises.find(ex => ex.id === session.exerciseId)
      return exercise?.tradition === tradition
    })
  }

  private saveSession(session: ReflectionSession): void {
    const sessions = this.getAllSessions()
    sessions.push(session)
    this.saveSessions(sessions)
  }

  private saveSessions(sessions: ReflectionSession[]): void {
    localStorage.setItem(this.SESSIONS_KEY, JSON.stringify(sessions))
  }

  exportSession(sessionId: string): string | null {
    const session = this.getSession(sessionId)
    const exercise = reflectionExercises.find(ex => ex.id === session?.exerciseId)
    
    if (!session || !exercise) return null

    const exportData = {
      exercise: {
        title: exercise.title,
        tradition: exercise.tradition,
        duration: exercise.duration
      },
      session: {
        startTime: session.startTime,
        endTime: session.endTime,
        duration: session.endTime 
          ? Math.round((session.endTime.getTime() - session.startTime.getTime()) / 1000 / 60)
          : null,
        mood: session.mood
      },
      responses: session.responses.map(response => ({
        question: exercise.steps.find(step => step.id === response.stepId)?.content || 'Unknown step',
        response: response.response,
        timestamp: response.timestamp
      })),
      insights: session.insights,
      nextSteps: session.nextSteps
    }

    return JSON.stringify(exportData, null, 2)
  }

  generatePersonalizedExercise(
    tradition: string,
    currentChallenges: string[],
    preferredDuration: number
  ): ReflectionExercise {
    // This would ideally use AI to generate personalized exercises
    // For now, return a customized version of an existing exercise
    const baseExercise = this.getRandomExercise(tradition, 'intermediate', preferredDuration)
    
    if (!baseExercise) {
      // Fallback to a general exercise
      return reflectionExercises[0]
    }

    return {
      ...baseExercise,
      id: `personalized-${Date.now()}`,
      title: `Personalized ${baseExercise.title}`,
      description: `A reflection tailored to your current challenges: ${currentChallenges.slice(0, 2).join(', ')}`
    }
  }
}

export const reflectionService = new ReflectionService()