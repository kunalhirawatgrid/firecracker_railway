import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Assessment from './pages/Assessment'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Assessment />} />
          <Route path="/assessment/:assessmentId" element={<Assessment />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

