# 🤖 Zoro AI

**Zoro AI** is a full-stack AI chatbot application built with **FastAPI** and **Streamlit**, featuring secure JWT authentication, persistent per-user chat history, a role-based admin dashboard, and an AI backend powered by **OpenRouter** — all while staying in character as Roronoa Zoro.

The project focuses on real-world backend development practices: REST API design, authentication, database modeling, migrations, rate limiting, and layered application architecture.

---

## ✨ Features

* 🤖 AI-powered conversational chatbot, always in character as Zoro
* 🔐 JWT-based authentication
* 🔑 Secure password hashing using Argon2
* 👤 User registration, signin, and self-service profile management
* 🛡️ Role-based access control (user / admin), with an admin dashboard for managing accounts
* 💬 Streaming chat interface built with Streamlit
* 🗄️ Supabase database integration
* 🧩 SQLAlchemy ORM for database operations
* 🔄 Alembic database migrations
* ⚡ FastAPI REST API backend
* 🚦 Per-endpoint rate limiting on auth routes
* ❤️ Health-check endpoint for uptime monitoring
* ⚙️ Environment-based configuration
* 🧱 Layered backend architecture

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │                     │
                    │  Signup / Signin    │
                    │  Chat / Profile /   │
                    │  Admin Dashboard    │
                    └──────────┬──────────┘
                               │
                         REST API / JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │     FastAPI         │
                    │      Backend        │
                    ├─────────────────────┤
                    │ Authentication      │
                    │ User Management     │
                    │ Chat API            │
                    │ Business Logic      │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐       ┌─────────────────┐
        │   PostgreSQL    │       │   OpenRouter    │
        │                 │       │      API        │
        │ Users / Chats   │       │ AI Responses    │
        └─────────────────┘       └─────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **Uvicorn**
* **slowapi** (rate limiting)

### Authentication & Security

* **JWT**
* **python-jose**
* **Argon2 password hashing**

### Database

* **Supabase**
* **SQLAlchemy ORM**
* **Alembic migrations**

### Frontend

* **Streamlit**

### AI

* **OpenRouter API** (model-agnostic LLM access, with automatic fallback across models)
* **HTTPX** (async streaming client)

### Development Tools

* **uv**
* **Git**
* **GitHub**

---

## 📁 Project Structure

```text
zoro-ai/
│
├── migrations/                 # Alembic migrations
│
├── src/
│   ├── backend/                 # FastAPI application
│   │   ├── main.py              # API entry point
│   │   └── ...
│   └── frontend/                # Streamlit application
│       ├── app.py               # Frontend entry point
│       └── ...
│
├── .env.example                 # Environment variable template
├── .gitignore
├── alembic.ini                  # Alembic configuration
├── pyproject.toml                # Project configuration & dependencies
├── uv.lock                        # Locked dependencies
└── README.md
```

---

## 🔐 Authentication Flow

Zoro AI uses JWT-based authentication to protect backend resources.

```text
User
 │
 ▼
Signup
 │
 ▼
Password hashed with Argon2
 │
 ▼
User stored in PostgreSQL
 │
 ▼
Signin
 │
 ▼
JWT Access Token
 │
 ▼
Streamlit stores authentication state
 │
 ▼
Protected API requests
 │
 ▼
FastAPI validates JWT
```

Passwords are never stored in plain text.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yashantthakurr/zoro-ai.git
cd zoro-ai
```

### 2. Install `uv`

If you don't already have `uv` installed:

```bash
pip install uv
```

### 3. Create the virtual environment

```bash
uv venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
uv sync
```

The project requires **Python 3.13+**.

---

## ⚙️ Environment Variables

Create a `.env` file from the provided example:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Example values:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/zoro_ai

ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
SECRET_KEY=your-secret-key

DEBUG=false

OPEN_ROUTER_API_KEY=your-openrouter-api-key
OPEN_ROUTER_MODEL=openai/gpt-4o-mini

ADMIN_EMAIL=admin@example.com
ADMIN_USERNAME=admin
ADMIN_PASSWORD=choose-a-strong-password

ZORO_API_BASE_URL=http://localhost:8000/api/v1
```

* `DEBUG` controls whether the interactive API docs (`/docs`, `/redoc`) are exposed — keep it `false` outside local development.
* `ADMIN_EMAIL` / `ADMIN_USERNAME` / `ADMIN_PASSWORD` seed the first admin account on startup, if that username doesn't already exist.
* `ZORO_API_BASE_URL` is read only by the Streamlit frontend, to know where to reach the API.

> Do not commit your `.env` file or real secrets to GitHub.

---

## 🗄️ Database Setup

Make sure PostgreSQL is running and the configured database exists.

Run the Alembic migrations:

```bash
uv run alembic upgrade head
```

To create a new migration after changing the database models:

```bash
uv run alembic revision --autogenerate -m "your migration message"
```

Then apply it:

```bash
uv run alembic upgrade head
```

---

## 🧠 OpenRouter Setup

Zoro AI uses **OpenRouter** to access LLMs without depending on a single provider.

1. Create an account at [openrouter.ai](https://openrouter.ai/) and generate an API key.
2. Set `OPEN_ROUTER_API_KEY` in your `.env` to that key.
3. Set `OPEN_ROUTER_MODEL` to the model slug you want as the primary model (browse available models and their current slugs at [openrouter.ai/models](https://openrouter.ai/models) — for example, `openai/gpt-4o-mini`).

If the primary model fails to respond, the backend automatically falls back through a short list of alternative models before giving up.

---

## ▶️ Running the Application

### Start the FastAPI backend

```bash
uv run uvicorn src.backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation (only available when `DEBUG=true`):

```text
http://127.0.0.1:8000/docs
```

A basic health check is always available at:

```text
http://127.0.0.1:8000/health
```

### Start the Streamlit frontend

In another terminal:

```bash
uv run streamlit run src/frontend/app.py
```

The Streamlit application will open in your browser.

---

## 🧪 API Testing

With `DEBUG=true`, the FastAPI backend provides interactive API documentation through Swagger UI:

```text
http://127.0.0.1:8000/docs
```

You can use it to test authentication and protected endpoints without requiring an external API client.

Postman can also be used for manual API testing.

---

## 🔄 Application Flow

```text
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Streamlit UI  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   FastAPI API   │
                  └───────┬─────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
                ▼                   ▼
        ┌──────────────┐    ┌──────────────┐
        │ PostgreSQL   │    │  OpenRouter  │
        │              │    │     API      │
        └──────────────┘    └──────────────┘
```

---

## 🎯 What I Learned

This project was built to gain practical experience in:

* Designing RESTful APIs with FastAPI
* Implementing JWT authentication
* Secure password hashing
* Database modeling with SQLAlchemy
* Managing database schema changes with Alembic
* Connecting a frontend application to a backend API
* Integrating a third-party LLM API with automatic model fallback
* Rate limiting sensitive endpoints
* Building role-based access control and an admin dashboard
* Managing authentication state in a frontend
* Structuring a backend application into maintainable modules
* Managing Python dependencies with `uv`

---

## 🔮 Future Improvements

Potential improvements include:

* [ ] Multiple conversation sessions per user
* [ ] Token usage tracking
* [ ] Redis-based caching
* [ ] Dockerized deployment
* [ ] Automated testing with Pytest
* [ ] CI/CD with GitHub Actions
* [ ] Production deployment

---

## 📌 Project Status

**Active Development**

Zoro AI is a learning-focused project designed around modern backend development and real-world AI integration.

---

## 👨‍💻 Author

**Yashant Thakur**

BCA Student | Backend Developer

* GitHub: https://github.com/yashantthakurr
* LinkedIn: https://linkedin.com/in/yashant-thakur/

---

## 📄 License

This project is intended for educational and portfolio purposes.