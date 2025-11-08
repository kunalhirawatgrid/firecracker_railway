import { useState, useEffect } from 'react';
import './Timer.css';

const Timer = ({ expiresAt, onExpire }) => {
  const [timeRemaining, setTimeRemaining] = useState(null);
  const [isExpired, setIsExpired] = useState(false);

  useEffect(() => {
    if (!expiresAt) {
      setTimeRemaining({ hours: 0, minutes: 0, seconds: 0 });
      return;
    }

    const updateTimer = () => {
      const now = new Date();
      // Handle ISO string with or without timezone
      const expiryStr = expiresAt.includes('Z') ? expiresAt : expiresAt + 'Z';
      const expiry = new Date(expiryStr);
      const diff = expiry - now;

      if (diff <= 0) {
        setIsExpired(true);
        setTimeRemaining({ hours: 0, minutes: 0, seconds: 0 });
        if (onExpire) {
          onExpire();
        }
        return;
      }

      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);

      setTimeRemaining({ hours, minutes, seconds });
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [expiresAt, onExpire]);

  if (!timeRemaining) {
    return <div className="timer">Loading...</div>;
  }

  const { hours, minutes, seconds } = timeRemaining;
  const isWarning = hours === 0 && minutes < 5;

  return (
    <div className={`timer ${isExpired ? 'expired' : ''} ${isWarning ? 'warning' : ''}`}>
      <div className="timer-label">Time Remaining</div>
      <div className="timer-display">
        {String(hours).padStart(2, '0')}:
        {String(minutes).padStart(2, '0')}:
        {String(seconds).padStart(2, '0')}
      </div>
      {isExpired && <div className="timer-expired">Time's Up!</div>}
    </div>
  );
};

export default Timer;

