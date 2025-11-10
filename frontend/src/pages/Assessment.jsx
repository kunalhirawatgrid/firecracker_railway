import React, { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import Timer from '../components/Timer'
import CodeEditor from '../components/CodeEditor'
import TestResults from '../components/TestResults'
import { getAssessment, executeWithTests } from '../services/assessmentApi'
import './Assessment.css'

const Assessment = () => {
  const { assessmentId } = useParams()
  const [assessment, setAssessment] = useState(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [submission, setSubmission] = useState(null)
  const [isRunning, setIsRunning] = useState(false)
  const [error, setError] = useState(null)
  const [timerActive, setTimerActive] = useState(true)

  useEffect(() => {
    loadAssessment()
  }, [assessmentId])

  useEffect(() => {
    // Initialize code for current question
    if (assessment && assessment.questions[currentQuestionIndex]) {
      const question = assessment.questions[currentQuestionIndex]
      if (question.allowed_languages.includes(language)) {
        // Code will be initialized by CodeEditor
      } else if (question.allowed_languages.length > 0) {
        setLanguage(question.allowed_languages[0])
      }
    }
  }, [currentQuestionIndex, assessment])

  const loadAssessment = async () => {
    try {
      // For demo, use a default assessment ID if none provided
      const id = assessmentId || 'default-assessment'
      const data = await getAssessment(id)
      setAssessment(data)
    } catch (err) {
      // If assessment not found, create a demo one
      console.log('Assessment not found, using demo data')
      setAssessment(getDemoAssessment())
    }
  }

  const getDemoAssessment = () => {
    return {
      id: 'default-assessment',
      created_at: new Date().toISOString(),
      title: 'Sample Coding Assessment',
      description: 'This is a sample assessment to demonstrate the platform',
      duration: 60,
      questions: [
        {
          id: 'q1',
          title: 'Two Sum',
          description:
            'Given an array of integers and a target sum, find two numbers that add up to the target. Return the indices of the two numbers.',
          difficulty: 'easy',
          sample_test_cases: [
            {
              id: 'tc1',
              input: '[2, 7, 11, 15]\n9',
              expected_output: '[0, 1]',
              type: 'sample',
            },
            {
              id: 'tc2',
              input: '[3, 2, 4]\n6',
              expected_output: '[1, 2]',
              type: 'sample',
            },
          ],
          hidden_test_cases: [
            {
              id: 'tc3',
              input: '[3, 3]\n6',
              expected_output: '[0, 1]',
              type: 'hidden',
            },
          ],
          allowed_languages: ['python', 'java', 'cpp', 'javascript'],
          time_limit: 30,
        },
      ],
    }
  }

  const handleRunCode = async () => {
    if (!assessment || !code.trim()) {
      setError('Please write some code first')
      return
    }

    setIsRunning(true)
    setError(null)
    setSubmission(null)

    try {
      const question = assessment.questions[currentQuestionIndex]
      const result = await executeWithTests(
        code,
        language,
        question.id,
        assessment.id,
        'candidate-1',
        false // Don't show hidden tests on run
      )
      setSubmission(result)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Execution failed')
      console.error('Execution error:', err)
    } finally {
      setIsRunning(false)
    }
  }

  const handleSubmit = async () => {
    if (!assessment || !code.trim()) {
      setError('Please write some code first')
      return
    }

    setIsRunning(true)
    setError(null)

    try {
      const question = assessment.questions[currentQuestionIndex]
      const result = await executeWithTests(
        code,
        language,
        question.id,
        assessment.id,
        'candidate-1',
        true // Include hidden tests on submit
      )
      setSubmission(result)
      alert(
        `Submission complete!\nSample Tests: ${result.sample_passed}/${result.sample_total}\nHidden Tests: ${result.hidden_passed}/${result.hidden_total}`
      )
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Submission failed')
      console.error('Submission error:', err)
    } finally {
      setIsRunning(false)
    }
  }

  const handleTimeUp = () => {
    setTimerActive(false)
    alert('Time is up! Your assessment has ended.')
  }

  if (!assessment) {
    return (
      <div className="assessment-loading">
        <div>Loading assessment...</div>
      </div>
    )
  }

  const currentQuestion = assessment.questions[currentQuestionIndex]

  return (
    <div className="assessment-container">
      <div className="assessment-header">
        <div className="header-content">
          <h1>{assessment.title}</h1>
          <p className="assessment-description">{assessment.description}</p>
        </div>
        <Timer
          duration={assessment.duration}
          onTimeUp={handleTimeUp}
          isActive={timerActive}
        />
      </div>

      <div className="assessment-body">
        <div className="questions-sidebar">
          <h3>Questions</h3>
          <div className="questions-list">
            {assessment.questions.map((q, index) => (
              <button
                key={q.id}
                className={`question-item ${
                  index === currentQuestionIndex ? 'active' : ''
                }`}
                onClick={() => {
                  setCurrentQuestionIndex(index)
                  setSubmission(null)
                  setError(null)
                }}
              >
                <span className="question-number">{index + 1}</span>
                <span className="question-title">{q.title}</span>
                <span className="question-difficulty">{q.difficulty}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="main-content">
          <div className="question-section">
            <div className="question-header">
              <h2>
                {currentQuestionIndex + 1}. {currentQuestion.title}
              </h2>
              <span className="difficulty-badge">
                {currentQuestion.difficulty}
              </span>
            </div>
            <div className="question-description">
              <pre>{currentQuestion.description}</pre>
            </div>

            <div className="sample-test-cases">
              <h4>Sample Test Cases</h4>
              {currentQuestion.sample_test_cases.map((tc, idx) => (
                <div key={tc.id} className="sample-test-case">
                  <div className="test-case-preview">
                    <div>
                      <strong>Input:</strong>
                      <pre>{tc.input}</pre>
                    </div>
                    <div>
                      <strong>Expected Output:</strong>
                      <pre>{tc.expected_output}</pre>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="code-section">
            <CodeEditor
              code={code}
              language={language}
              onChange={setCode}
              onLanguageChange={setLanguage}
            />
            <div className="code-actions">
              <button
                className="btn btn-run"
                onClick={handleRunCode}
                disabled={isRunning || !code.trim()}
              >
                {isRunning ? 'Running...' : 'Run Code'}
              </button>
              <button
                className="btn btn-submit"
                onClick={handleSubmit}
                disabled={isRunning || !code.trim()}
              >
                {isRunning ? 'Submitting...' : 'Submit'}
              </button>
            </div>
            {error && <div className="error-message">{error}</div>}
          </div>

          <div className="results-section">
            <TestResults
              submission={submission}
              showHidden={false} // Only show hidden on submit
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Assessment

