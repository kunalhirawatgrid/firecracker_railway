import React, { useState } from 'react'
import './TestResults.css'

const TestResults = ({ submission, showHidden = false }) => {
  const [expandedTests, setExpandedTests] = useState(new Set())

  if (!submission) {
    return (
      <div className="test-results">
        <div className="test-results-placeholder">
          Run your code to see test results
        </div>
      </div>
    )
  }

  const toggleTest = (testId) => {
    const newExpanded = new Set(expandedTests)
    if (newExpanded.has(testId)) {
      newExpanded.delete(testId)
    } else {
      newExpanded.add(testId)
    }
    setExpandedTests(newExpanded)
  }

  // Test results are ordered: sample tests first, then hidden tests
  const sampleResults = submission.test_results.slice(0, submission.sample_total)
  const hiddenResults = submission.test_results.slice(submission.sample_total)

  const visibleResults = showHidden
    ? [...sampleResults, ...hiddenResults]
    : sampleResults

  return (
    <div className="test-results">
      <div className="test-results-header">
        <h3>Test Results</h3>
        <div className="test-summary">
          <div className="summary-item">
            <span className="summary-label">Sample Tests:</span>
            <span className="summary-value">
              {submission.sample_passed}/{submission.sample_total} passed
            </span>
          </div>
          {showHidden && (
            <div className="summary-item">
              <span className="summary-label">Hidden Tests:</span>
              <span className="summary-value">
                {submission.hidden_passed}/{submission.hidden_total} passed
              </span>
            </div>
          )}
        </div>
      </div>

      {submission.compilation_logs && (
        <div className="compilation-logs">
          <div className="logs-header">Compilation Logs</div>
          <pre className="logs-content">{submission.compilation_logs}</pre>
        </div>
      )}

      <div className="test-cases">
        {visibleResults.map((testResult, index) => {
          const isExpanded = expandedTests.has(testResult.test_case_id)
          // Check if this is a hidden test case (appears after sample tests in the full list)
          const isHidden = showHidden && index >= submission.sample_total

          return (
            <div
              key={testResult.test_case_id}
              className={`test-case ${testResult.passed ? 'passed' : 'failed'} ${
                isHidden ? 'hidden' : ''
              }`}
            >
              <div
                className="test-case-header"
                onClick={() => toggleTest(testResult.test_case_id)}
              >
                <div className="test-case-status">
                  <span className="status-icon">
                    {testResult.passed ? '✓' : '✗'}
                  </span>
                  <span className="test-case-name">
                    Test Case {index + 1}
                    {isHidden && ' (Hidden)'}
                  </span>
                </div>
                <div className="test-case-meta">
                  {testResult.execution_time && (
                    <span className="execution-time">
                      {testResult.execution_time.toFixed(3)}s
                    </span>
                  )}
                  <span className="expand-icon">
                    {isExpanded ? '▼' : '▶'}
                  </span>
                </div>
              </div>

              {isExpanded && (
                <div className="test-case-details">
                  <div className="test-detail">
                    <div className="test-detail-label">Input:</div>
                    <pre className="test-detail-value">{testResult.input}</pre>
                  </div>
                  <div className="test-detail">
                    <div className="test-detail-label">Expected Output:</div>
                    <pre className="test-detail-value">
                      {testResult.expected_output}
                    </pre>
                  </div>
                  <div className="test-detail">
                    <div className="test-detail-label">Your Output:</div>
                    <pre className="test-detail-value">
                      {testResult.actual_output || '(empty)'}
                    </pre>
                  </div>
                  {testResult.error && (
                    <div className="test-detail">
                      <div className="test-detail-label">Error:</div>
                      <pre className="test-detail-value error">
                        {testResult.error}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default TestResults

