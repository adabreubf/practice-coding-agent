import { createContext, useContext, useState, useCallback } from 'react';

const AuthContext = createContext(null);

const SESSION_KEY = 'cp_access_token';
const SESSION_USER_KEY = 'cp_username';

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => sessionStorage.getItem(SESSION_KEY));
  const [username, setUsername] = useState(() => sessionStorage.getItem(SESSION_USER_KEY));

  const login = useCallback(async (user, password) => {
    const response = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, password }),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data.detail || 'Invalid credentials');
    }

    const data = await response.json();
    sessionStorage.setItem(SESSION_KEY, data.access_token);
    sessionStorage.setItem(SESSION_USER_KEY, user);
    setToken(data.access_token);
    setUsername(user);
    return data;
  }, []);

  const logout = useCallback(() => {
    sessionStorage.removeItem(SESSION_KEY);
    sessionStorage.removeItem(SESSION_USER_KEY);
    setToken(null);
    setUsername(null);
  }, []);

  const isAuthenticated = Boolean(token);

  return (
    <AuthContext.Provider value={{ token, username, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
