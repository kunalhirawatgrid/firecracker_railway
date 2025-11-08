import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Assessment from './pages/Assessment';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/assessment/:assessmentId" element={<Assessment />} />
        <Route path="/" element={<Navigate to="/assessment/1?candidate_id=candidate_1" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
