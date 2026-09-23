# 🤖 Zoro AI

**Zoro AI** is a full-stack AI chatbot application built with **FastAPI** and **Streamlit**, featuring secure user authentication, persistent user data, and integration with a locally hosted Large Language Model (LLM).

The project focuses on building an AI-powered application while applying real-world backend development practices such as REST API design, authentication, database management, migrations, and API load testing.

---

## ✨ Features

* 🤖 AI-powered conversational chatbot
* 🔐 JWT-based authentication
* 🔑 Secure password hashing using Argon2
* 👤 User registration and authentication
* 🛡️ Protected API endpoints
* 💬 Chat interface built with Streamlit
* 🗄️ PostgreSQL database integration
* 🧩 SQLAlchemy ORM for database operations
* 🔄 Alembic database migrations
* ⚡ FastAPI REST API backend
* 📊 API load testing with Locust
* ⚙️ Environment-based configuration
* 🧱 Layered backend architecture

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │                     │
                    │  Signup / Signin    │
                    │  Chat / Profile     │
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
        │   PostgreSQL    │       │   Local LLM     │
        │                 │       │                 │
        │ Users / Data    │       │ AI Responses    │
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

### Authentication & Security

* **JWT**
* **python-jose**
* **Argon2 password hashing**

### Database

* **PostgreSQL**
* **SQLAlchemy ORM**
* **Alembic migrations**

### Frontend

* **Streamlit**

### AI

* **Local LLM integration**
* **Ollama**

### Testing & Performance

* **Locust**
* **HTTPX**

### Development Tools

* **uv**
* **Git**
* **GitHub**

---

## 📁 Project Structure

```text
zoro-ai/
│
├── migrations/
│   └── ...                    # Alembic migrations
│
├── src/
│   └── ...
│
├── .env.example               # Environment variable template
├── .gitignore
├── alembic.ini                # Alembic configuration
├── pyproject.toml              # Project configuration & dependencies
├── server.py                   # FastAPI application entry point
├── uv.lock                     # Locked dependencies
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

Configure the required values in `.env`, including your database connection and JWT configuration.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/zoro_ai

JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=30

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=your-model
```

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

## 🧠 Ollama Setup

Zoro AI is designed to use a locally hosted LLM through **Ollama**.

Install Ollama from:

https://ollama.com/

Then download the model you want to use:

```bash
ollama pull <model-name>
```

Start Ollama if it is not already running:

```bash
ollama serve
```

Make sure the model configured in your `.env` matches the model installed locally.

---

## ▶️ Running the Application

### Start the FastAPI backend

```bash
uv run uvicorn server:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### Start the Streamlit frontend

In another terminal:

```bash
uv run streamlit run src/app.py
```

The Streamlit application will open in your browser.

---

## 🧪 API Testing

The FastAPI backend provides interactive API documentation through Swagger UI:

```text
http://127.0.0.1:8000/docs
```

You can use it to test authentication and protected endpoints without requiring an external API client.

Postman can also be used for manual API testing.

---

## 📊 Load Testing

Zoro AI includes **Locust** for testing API performance under concurrent requests.

Start Locust with:

```bash
uv run locust
```

Then open:

```text
http://localhost:8089
```

Configure the target API host and number of concurrent users from the Locust interface.

This allows the backend to be evaluated under simulated concurrent traffic.

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
        │ PostgreSQL   │    │  Local LLM   │
        │              │    │   Ollama     │
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
* Integrating locally hosted LLMs
* Managing authentication state in a frontend
* Structuring a backend application into maintainable modules
* Load testing APIs with Locust
* Managing Python dependencies with `uv`

---

## 🔮 Future Improvements

Potential improvements include:

* [ ] Conversation history and chat persistence
* [ ] Streaming LLM responses
* [ ] Multiple conversation sessions
* [ ] Token usage tracking
* [ ] Improved error handling
* [ ] API rate limiting
* [ ] Redis-based caching
* [ ] Dockerized deployment
* [ ] Automated testing with Pytest
* [ ] CI/CD with GitHub Actions
* [ ] Production deployment

---

## 📌 Project Status

**Active Development**

Zoro AI is a learning-focused project designed around modern backend development and local AI integration.

---

## 👨‍💻 Author

**Yashant Thakur**

BCA Student | Backend Developer

* GitHub: https://github.com/yashantthakurr
* LinkedIn: https://linkedin.com/in/yashant-thakur/

---

## 📄 License

This project is intended for educational and portfolio purposes.
