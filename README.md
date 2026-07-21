# Expense Tracker API

A production-ready Expense Tracker REST API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Docker**.

## Features

- User Authentication (JWT)
- User Registration & Login
- Expense CRUD Operations
- PostgreSQL Database
- SQLAlchemy ORM
- Alembic Database Migrations
- Docker & Docker Compose
- Kubernetes Deployment
- Redis Integration
- Celery Background Tasks
- RESTful API
- Interactive Swagger Documentation

---

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Docker Compose
- Kubernetes
- Redis
- Celery
- Git & GitHub

---

## Project Structure

```text
expense-tracker-api/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── middleware/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/Apn09/expense-tracker-api.git
```

Move into the project

```bash
cd expense-tracker-api
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment

macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file using `.env.example`.

Example

```envexample
DATABASE_URL=postgresql://expense_user:expense_password@localhost:5432/expense_tracker
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up -d
```

---

## API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

## Future Enhancements

- Expense Categories
- Monthly Reports
- Email Notifications
- Budget Management
- Analytics Dashboard
- CI/CD Pipeline
- Kubernetes Deployment
- Monitoring with Prometheus & Grafana

---

## Author

Anandhapadmanaban
