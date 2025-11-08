import { useState, useEffect } from 'react';
import api from './services/api';
import './App.css';

function App() {
  const [healthStatus, setHealthStatus] = useState(null);
  const [exampleData, setExampleData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Check API health on mount
    checkHealth();
    fetchExample();
  }, []);

  const checkHealth = async () => {
    try {
      const data = await api.health();
      setHealthStatus(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchExample = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getExample();
      setExampleData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePostExample = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.postExample({ message: 'Hello from frontend!' });
      setExampleData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Firecracker Railway</h1>
        <p>FastAPI + React + Vite</p>
      </header>

      <main className="app-main">
        <section className="status-section">
          <h2>API Status</h2>
          {healthStatus ? (
            <div className="status-card success">
              <p>Status: {healthStatus.status}</p>
              <p>Service: {healthStatus.service}</p>
            </div>
          ) : (
            <div className="status-card">Checking...</div>
          )}
        </section>

        <section className="example-section">
          <h2>Example API Call</h2>
          <div className="button-group">
            <button onClick={fetchExample} disabled={loading}>
              {loading ? 'Loading...' : 'Fetch Example'}
            </button>
            <button onClick={handlePostExample} disabled={loading}>
              {loading ? 'Sending...' : 'Post Example'}
            </button>
          </div>

          {error && (
            <div className="error-message">
              <p>Error: {error}</p>
            </div>
          )}

          {exampleData && (
            <div className="data-card">
              <pre>{JSON.stringify(exampleData, null, 2)}</pre>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
