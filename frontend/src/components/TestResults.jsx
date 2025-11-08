const TestResults = ({ results, compilationLogs, executionLogs }) => {
  if (!results || results.length === 0) {
    return null;
  }

  const passedCount = results.filter((r) => r.passed).length;
  const totalCount = results.length;

  return (
    <div className="test-results">
      <div className="test-results-header">
        <h3>Test Results</h3>
        <div className="test-summary">
          {passedCount} / {totalCount} test cases passed
        </div>
      </div>

      {(compilationLogs || executionLogs) && (
        <div className="logs-section">
          {compilationLogs && compilationLogs.trim() && (
            <div className="compilation-logs">
              <h4>Compilation Logs</h4>
              <pre>{compilationLogs}</pre>
            </div>
          )}
          {executionLogs && executionLogs.trim() && (
            <div className="execution-logs">
              <h4>Execution Output</h4>
              <pre>{executionLogs}</pre>
            </div>
          )}
        </div>
      )}

      <div className="test-cases">
        {results.map((result, index) => (
          <div
            key={result.test_case_id || index}
            className={`test-case ${result.passed ? 'passed' : 'failed'}`}
          >
            <div className="test-case-header">
              <span className="test-case-type">
                {result.is_sample ? 'Sample' : 'Hidden'} Test Case
              </span>
              <span className={`test-case-status ${result.passed ? 'passed' : 'failed'}`}>
                {result.passed ? '✓ Passed' : '✗ Failed'}
              </span>
            </div>
            {result.error && (
              <div className="test-case-error">
                <strong>Error:</strong> {result.error}
              </div>
            )}
            {result.expected_output && (
              <div className="test-case-output">
                <div>
                  <strong>Expected:</strong>
                  <pre>{result.expected_output}</pre>
                </div>
                {result.actual_output !== null && (
                  <div>
                    <strong>Actual:</strong>
                    <pre>{result.actual_output || '(no output)'}</pre>
                  </div>
                )}
              </div>
            )}
            {result.execution_time_ms && (
              <div className="test-case-time">
                Execution time: {result.execution_time_ms}ms
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TestResults;

