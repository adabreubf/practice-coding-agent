# Compliance Platform — Frontend

A React + Vite single-page application (SPA) that provides a **login page** and a **welcome page** for the Compliance Platform. It authenticates against the FastAPI backend using JWT tokens and stores the session securely in the browser's Session Storage.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Design System](#design-system)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Environment & Configuration](#environment--configuration)
- [Usage](#usage)
- [Build for Production](#build-for-production)

---

## Features

- **Login page** — Authenticates via `POST /auth/login` and stores the JWT access token in `sessionStorage`.
- **Welcome page** — Protected route; only accessible when a valid session token exists.
- **Session management** — Token and username are cleared from `sessionStorage` on sign-out.
- **Automatic redirect** — Unauthenticated access to `/welcome` redirects back to `/login`.
- **Design system** — Follows the Compliance Platform design spec (Inter typography, glass surfaces, gradient border shells, ambient background).

---

## Project Structure

```
frontend/
├── src/
│   ├── context/
│   │   └── AuthContext.jsx    # Auth state + sessionStorage helpers
│   ├── components/
│   │   └── ProtectedRoute.jsx # Route guard for authenticated pages
│   ├── pages/
│   │   ├── LoginPage.jsx      # Login form
│   │   ├── LoginPage.css
│   │   ├── WelcomePage.jsx    # Welcome / dashboard page
│   │   └── WelcomePage.css
│   ├── App.jsx                # Router + providers
│   ├── main.jsx               # React entry point
│   └── index.css              # Global design tokens
├── index.html
├── vite.config.js             # Dev proxy to backend at :8000
└── package.json
```

---

## Design System

The UI follows the **Compliance Platform** design spec defined in `../Compliance-Platform-DESIGN.md`:

| Token | Value |
|---|---|
| Primary | `#0F172A` |
| Secondary | `#E0E7FF` |
| Background | `#FAFAFA` |
| Surface | `#F8F9FA` |
| Text secondary | `#64748B` |
| Border | `#F1F5F9` |
| Base spacing | 12 px |
| Font | Inter |
| Surface style | Glass (backdrop-filter blur 12 px) |
| Elevation | Gradient border shell |

---

## Prerequisites

- **Node.js** >= 18 (LTS recommended)
- **npm** >= 9
- The **backend** running locally on `http://localhost:8000` (see the backend README)

---

## Getting Started

### 1. Start the backend

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
# API available at http://localhost:8000
```

### 2. Install frontend dependencies

```bash
cd frontend
npm install
```

### 3. Start the development server

```bash
npm run dev
# App available at http://localhost:5173
```

The Vite dev server proxies `/auth/*` requests to `http://localhost:8000`, so no CORS configuration is needed in development.

---

## Environment & Configuration

| Setting | Default | Description |
|---|---|---|
| Backend URL | `http://localhost:8000` | Configured in `vite.config.js` proxy |
| Session key | `cp_access_token` | Key used to store the JWT in sessionStorage |

The backend credentials are set via environment variables (see `backend/README.md`):

| Variable | Default |
|---|---|
| `JWT_ADMIN_USERNAME` | `admin` |
| `JWT_ADMIN_PASSWORD` | `admin123` |

---

## Usage

1. Open `http://localhost:5173` in your browser — you will be redirected to `/login`.
2. Enter your credentials (`admin` / `admin123` by default).
3. On success, you are redirected to `/welcome`.
4. The access token is stored in `sessionStorage` for the duration of the browser tab.
5. Click **Sign out** to clear the session and return to the login page.
6. Closing the browser tab removes the token automatically (sessionStorage lifetime).

---

## Build for Production

```bash
npm run build
# Output in frontend/dist/
npm run preview  # local preview of the production build
```

For production, configure a reverse proxy (Nginx, Caddy, etc.) to:
- Serve `frontend/dist/` as static files.
- Forward `/auth/*` to the backend service.
- Add appropriate CORS headers if the frontend and backend are on different origins.
