# 🌍 GlobeMaster

**GlobeMaster** is a full-stack geography quiz game built with **React**, **Flask**, and **PostgreSQL**.  
Players create a profile, play timed quiz sessions by category and difficulty, earn badges, and have their progress persisted across games.

This project was built as a **portfolio-grade, end-to-end Python application**, emphasizing clean backend logic, real database relationships, and a playable frontend experience.

---

## 🎯 Core Features

- 🎮 Play full quiz sessions end-to-end
- 🧭 Category-based and difficulty-based questions
- 🧠 Backend-validated answers and scoring
- 🏅 Badge system (first launch, milestones, achievements)
- 📊 Persistent game sessions and player history
- 🔁 Resume-safe gameplay (server-side state)
- 🧑‍💻 Clean API consumed by a React frontend

---

## 🛠️ Tech Stack

| Layer | Technology |
|-----|-----------|
| Frontend | React + Vite |
| Backend | Python · Flask · SQLAlchemy |
| Database | PostgreSQL |
| Hosting | **Heroku (monolithic deployment)** |

> The frontend build is served by the Flask backend in production.

---

## 🧩 Architecture Overview

GlobeMaster is intentionally deployed as a **monolith**:

- One Flask application
- One PostgreSQL database
- One deployed service

This matches the scale and scope of the project and avoids unnecessary infrastructure complexity while remaining production-ready.

**Key design principles:**
- Backend is the source of truth
- No game logic trusted to the client
- Database models reflect real relationships
- API is clean, explicit, and testable

---

## 🗂️ Data Model

Core entities include:

- **Player**
- **Profile**
- **GameSession**
- **Question**
- **GameSessionQuestion**
- **Badge**
- **PlayerBadge**

The database schema for GlobeMaster is illustrated below:

![GlobeMaster ERD](./globemaster_erd.png)

---

## 🚀 Deployment

GlobeMaster is deployed as a **single Heroku application**:

- Flask serves the API and the built React frontend
- PostgreSQL is provided via Heroku Postgres
- Configuration is handled through environment variables

There is **no Docker requirement** for deployment.

---

## 🧪 Example API Endpoints

- `GET /meta/health` – Health check
- `GET /meta/categories` – Available quiz categories
- `POST /players` – Create player
- `GET /players/email/<email>` – Load player
- `POST /games` – Start a new game session
- `POST /game-session-questions` – Submit an answer
- `GET /badges/player/<id>` – Player achievements

---

## 🎥 Demo Video

> **Demo video coming soon**

**[ PLACEHOLDER – New walkthrough video will be added here ]**

---

## 📜 License

MIT License.
