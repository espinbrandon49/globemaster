# 🌐 GlobeMaster

**GlobeMaster** is a full-stack geography quiz game built with React, Flask, PostgreSQL, and Docker. Players answer questions by category or preferred difficulty, earn badges, and track their performance across persistent game sessions.

---

## 🚀 Features

- ✅ 10-question quiz rounds
- ✅ Categories and difficulty-based question filtering
- ✅ Backend-driven scoring with persistent sessions
- ✅ Badges awarded for first launch, perfect scores, and category mastery
- ✅ Fully Dockerized setup for easy local development
- ✅ Responsive UI with dynamic feedback and profile info
- ✅ State persistence across reloads

---

## 🛠️ Tech Stack

| Layer     | Technology                         |
|-----------|-------------------------------------|
| Frontend  | React + Vite                       |
| Backend   | Flask + SQLAlchemy                 |
| Database  | PostgreSQL                         |
| Container | Docker + Docker Compose            |

---

## 🧩 Project Structure

```
globemaster/
├── backend/
│   ├── app/               # Flask app (routes, models, utils)
│   ├── seed.py            # Sample questions seeder
│   ├── Dockerfile         # Backend image
│   └── .env               # Database URL (ignored by Git)
├── frontend/
│   ├── src/               # React components
│   ├── Dockerfile.frontend
├── docker-compose.yml     # Project orchestrator
```

---

## ⚙️ Local Development

### 1. Clone the repo

```bash
git clone https://github.com/espinbrandon49/globemaster.git
cd globemaster
```

### 2. Add your `.env` file

Create `backend/.env`:

```
DATABASE_URL=postgresql://postgres:password@db:5432/globemaster
```

> ⚠️ This file is ignored via `.gitignore`

### 3. Start the stack

```bash
docker-compose up --build
```

- Frontend → [http://localhost:5173](http://localhost:5173)
- Backend API → [http://localhost:5000](http://localhost:5000)

---

## 🧪 Sample Endpoints

- `GET /games/<id>` – Retrieve game session info
- `POST /game_questions/` – Record player answer
- `PUT /games/<id>` – (Optional) Update session stats
- `GET /badges/player/<id>` – View earned badges

---

## 🧠 Design Notes

GlobeMaster emphasizes backend-first logic:
- Score and game progress are always stored server-side
- Frontend uses localStorage only for session handoff
- React auto-resumes progress after a page reload

---

## 📸 Screenshots (optional)

> *(Add later: Home screen, question view, badge modal, etc.)*

---

## 📜 License

MIT License. Built with 🚀, 🧠, and a slight obsession with global trivia.
