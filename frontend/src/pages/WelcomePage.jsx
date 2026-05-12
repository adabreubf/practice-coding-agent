import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './WelcomePage.css';

export default function WelcomePage() {
  const { username, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <div className="welcome-bg">
      <div className="welcome-ambient" aria-hidden="true">
        <div className="welcome-blob wblob-1" />
        <div className="welcome-blob wblob-2" />
      </div>

      <div className="welcome-layout">
        {/* Top bar */}
        <header className="welcome-topbar">
          <div className="topbar-brand">
            <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
              <rect width="32" height="32" rx="8" fill="#0F172A" />
              <path
                d="M8 16c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8-8-3.582-8-8z"
                stroke="#E0E7FF"
                strokeWidth="1.5"
                fill="none"
              />
              <path d="M13 16l2 2 4-4" stroke="#E0E7FF" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span className="topbar-name">Compliance Platform</span>
          </div>
          <div className="topbar-actions">
            <span className="topbar-user">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <circle cx="8" cy="5.5" r="2.5" stroke="#64748B" strokeWidth="1.25" />
                <path d="M3 13c0-2.761 2.239-5 5-5s5 2.239 5 5" stroke="#64748B" strokeWidth="1.25" strokeLinecap="round" />
              </svg>
              {username}
            </span>
            <button className="topbar-logout" onClick={handleLogout}>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M6 2H3a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" />
                <path d="M10 11l3-3-3-3M13 8H6" stroke="currentColor" strokeWidth="1.25" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
              Sign out
            </button>
          </div>
        </header>

        {/* Main content */}
        <main className="welcome-main">
          <div className="welcome-shell">
            <div className="welcome-card">
              <div className="welcome-badge">Authenticated</div>
              <h1 className="welcome-heading">Welcome back{username ? `, ${username}` : ''}.</h1>
              <p className="welcome-body">
                You are successfully signed in to the Compliance Platform. Your session is active
                and your access token is securely stored for this session.
              </p>

              <div className="welcome-stats">
                <div className="stat-item">
                  <span className="stat-label">Session status</span>
                  <span className="stat-value stat-active">
                    <span className="stat-dot" aria-hidden="true" />
                    Active
                  </span>
                </div>
                <div className="stat-divider" aria-hidden="true" />
                <div className="stat-item">
                  <span className="stat-label">Token stored in</span>
                  <span className="stat-value">Session Storage</span>
                </div>
                <div className="stat-divider" aria-hidden="true" />
                <div className="stat-item">
                  <span className="stat-label">Token expires in</span>
                  <span className="stat-value">300 s</span>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
