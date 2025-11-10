import React, { useState, useEffect } from 'react'
import './Timer.css'

const Timer = ({ duration, onTimeUp, isActive = true }) => {
  const [timeLeft, setTimeLeft] = useState(duration * 60) // Convert minutes to seconds

  useEffect(() => {
    if (!isActive || timeLeft <= 0) {
      if (timeLeft <= 0 && onTimeUp) {
        onTimeUp()
      }
      return
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          if (onTimeUp) {
            onTimeUp()
          }
          return 0
        }
        return prev - 1
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [timeLeft, isActive, onTimeUp])

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60

    if (hours > 0) {
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    }
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }

  const getTimeColor = () => {
    if (timeLeft <= 300) return 'red' // Less than 5 minutes
    if (timeLeft <= 900) return 'orange' // Less than 15 minutes
    return 'green'
  }

  return (
    <div className={`timer ${getTimeColor()}`}>
      <div className="timer-label">Time Remaining</div>
      <div className="timer-value">{formatTime(timeLeft)}</div>
    </div>
  )
}

export default Timer

