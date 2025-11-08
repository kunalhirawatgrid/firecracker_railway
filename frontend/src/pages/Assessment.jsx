import { useState, useEffect } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import CodeEditor from '../components/CodeEditor';
import Timer from '../components/Timer';
import TestResults from '../components/TestResults';
import { assessmentApi } from '../services/assessmentApi';
import './Assessment.css';

const Assessment = () => {
  const { assessmentId } = useParams();
  const [searchParams] = useSearchParams();
  const candidateId = searchParams.get('candidate_id') || 'candidate_1';

  const [assessment, setAssessment] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [submission, setSubmission] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    loadAssessment();
  }, [assessmentId, candidateId]);

  const loadAssessment = async () => {
    try {
      const [assessmentRes, questionsRes] = await Promise.all([
        assessmentApi.getAssessment(assessmentId, candidateId),
        assessmentApi.getQuestions(assessmentId, candidateId),
      ]);
      
      const assessmentData = assessmentRes.data.data || assessmentRes.data;
      setAssessment(assessmentData);
      setQuestions(questionsRes.data.data || questionsRes.data);
      
      // Start assessment if not started
      if (assessmentData.status === 'not_started') {
        await startAssessment();
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load assessment');
    }
  };

  const startAssessment = async () => {
    try {
      const response = await assessmentApi.startAssessment(assessmentId, candidateId);
      setAssessment(response.data.data || response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start assessment');
    }
  };

  const handleRunCode = async () => {
    if (!code.trim()) {
      setError('Please write some code first');
      return;
    }

    setIsRunning(true);
    setError(null);
    setSubmission(null);

    try {
      const currentQuestion = questions[currentQuestionIndex];
      const response = await assessmentApi.submitSolution(
        assessmentId,
        currentQuestion.id,
        candidateId,
        {
          code,
          language,
        }
      );
      setSubmission(response.data.data || response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to run code');
    } finally {
      setIsRunning(false);
    }
  };

  const handleTestCode = async () => {
    if (!code.trim()) {
      setError('Please write some code first');
      return;
    }

    setIsRunning(true);
    setError(null);

    try {
      const response = await assessmentApi.executeCode({
        code,
        language,
      });
      const result = response.data.data || response.data;
      setSubmission({
        test_results: [],
        compilation_logs: result.stderr,
        execution_logs: result.stdout,
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to test code');
    } finally {
      setIsRunning(false);
    }
  };

  const currentQuestion = questions[currentQuestionIndex];

  if (!assessment || questions.length === 0) {
    return <div className="assessment-loading">Loading assessment...</div>;
  }

  return (
    <div className="assessment-container">
      <div className="assessment-header">
        <h1>{assessment.title}</h1>
        {assessment.expires_at && (
          <Timer
            expiresAt={assessment.expires_at}
            onExpire={() => {
              setError('Assessment time has expired');
            }}
          />
        )}
      </div>

      <div className="assessment-content">
        <div className="assessment-sidebar">
          <div className="questions-list">
            <h3>Questions</h3>
            {questions.map((q, index) => (
              <button
                key={q.id}
                className={`question-item ${index === currentQuestionIndex ? 'active' : ''}`}
                onClick={() => setCurrentQuestionIndex(index)}
              >
                <span className="question-number">{index + 1}</span>
                <span className="question-title">{q.title}</span>
                <span className="question-difficulty">{q.difficulty}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="assessment-main">
          {currentQuestion && (
            <>
              <div className="question-section">
                <div className="question-header">
                  <h2>
                    Question {currentQuestionIndex + 1}: {currentQuestion.title}
                  </h2>
                  <span className="difficulty-badge">{currentQuestion.difficulty}</span>
                </div>
                <div className="question-description">
                  <pre>{currentQuestion.description}</pre>
                </div>
                {currentQuestion.test_cases
                  .filter((tc) => tc.is_sample)
                  .map((tc, index) => (
                    <div key={tc.id} className="sample-test-case">
                      <h4>Sample Test Case {index + 1}</h4>
                      <div>
                        <strong>Input:</strong>
                        <pre>{tc.input_data}</pre>
                      </div>
                      <div>
                        <strong>Expected Output:</strong>
                        <pre>{tc.expected_output}</pre>
                      </div>
                    </div>
                  ))}
              </div>

              <div className="code-section">
                <div className="code-header">
                  <select
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="language-select"
                  >
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="javascript">JavaScript</option>
                  </select>
                  <div className="code-actions">
                    <button
                      onClick={handleTestCode}
                      disabled={isRunning}
                      className="btn-test"
                    >
                      Test Code
                    </button>
                    <button
                      onClick={handleRunCode}
                      disabled={isRunning}
                      className="btn-submit"
                    >
                      {isRunning ? 'Running...' : 'Run & Submit'}
                    </button>
                  </div>
                </div>
                <CodeEditor
                  code={code}
                  language={language}
                  onChange={setCode}
                />
              </div>

              {error && <div className="error-message">{error}</div>}

              {submission && (
                <div className="submission-results">
                  <TestResults
                    results={submission.test_results || []}
                    compilationLogs={submission.compilation_logs || ''}
                    executionLogs={submission.execution_logs || ''}
                  />
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Assessment;

