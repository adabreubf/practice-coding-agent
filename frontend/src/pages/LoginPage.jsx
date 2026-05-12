import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './LoginPage.css';

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      navigate('/welcome');
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-bg">
      {/* Ambient background canvas fallback */}
      <div className="login-ambient" aria-hidden="true">
        <div className="ambient-blob blob-1" />
        <div className="ambient-blob blob-2" />
      </div>

      <main className="login-center">
        {/* Gradient border shell */}
        <div className="login-shell">
          <div className="login-card">
            <header className="login-header">
              <div className="login-logo" aria-hidden="true">
                <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                  <rect width="32" height="32" rx="8" fill="#0F172A" />
                  <path
                    d="M8 16c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8-8-3.582-8-8z"
                    stroke="#E0E7FF"
                    strokeWidth="1.5"
                    fill="none"
                  />
                  <path d="M13 16l2 2 4-4" stroke="#E0E7FF" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h1 className="login-title">Compliance Platform</h1>
              <p className="login-subtitle">Sign in to your account</p>
            </header>

            <form className="login-form" onSubmit={handleSubmit} noValidate>
              <div className="field-group">
                <label className="field-label" htmlFor="username">Username</label>
                <input
                  id="username"
                  className="field-input"
                  type="text"
                  autoComplete="username"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                  required
                  disabled={loading}
                  placeholder="Enter your username"
                />
              </div>

              <div className="field-group">
                <label className="field-label" htmlFor="password">Password</label>
                <input
                  id="password"
                  className="field-input"
                  type="password"
                  autoComplete="current-password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                  disabled={loading}
                  placeholder="Enter your password"
                />
              </div>

              {error && (
                <div className="login-error" role="alert">
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                    <circle cx="8" cy="8" r="7" stroke="#DC2626" strokeWidth="1.5" />
                    <path d="M8 5v4M8 11v.5" stroke="#DC2626" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                  {error}
                </div>
              )}

              <button className="login-btn" type="submit" disabled={loading || !username || !password}>
                {loading ? (
                  <span className="btn-spinner" aria-hidden="true" />
                ) : null}
                {loading ? 'Signing in…' : 'Sign in'}
              </button>
            </form>
          </div>
        </div>
      </main>
    </div>
  );
}
