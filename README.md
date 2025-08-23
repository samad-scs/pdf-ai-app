# DocuLearn

A production-ready backend project built with **FastAPI** .

This project is designed as a learning journey to explore FastAPI’s features, best practices, and ecosystem — while also serving as a reusable boilerplate for real-world applications.

## ✨ Features (planned and implemented)

- [x] FastAPI app structure (`src/` based modular layout)
- [x] Auto-generated API docs with **Swagger UI** and **ReDoc**
- [ ] User authentication with session management
- [ ] Database integration (SQLAlchemy + Alembic migrations)
- [ ] Environment-based configuration (`.env` support)
- [ ] Docker & Docker Compose for easy deployment
- [ ] Testing with `pytest`
- [ ] CI/CD setup (GitHub Actions)

## 📂 Project Structure (early draft)

```
fastapi-production-starter/
│── src/
│   ├── main.py         # Entry point
│   ├── api/            # API routes
│   ├── core/           # Config & settings
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   └── utils/          # Helper functions
│
│── tests/              # Test cases
│── requirements.txt    # Dependencies
│── .env.example        # Example env file
│── README.md           # Project documentation
│── .gitignore
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fastapi-production-starter.git
cd fastapi-production-starter
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```

### 3. Run the development server

```bash
uvicorn src.main:app --reload
```

Visit:

- Swagger UI → `http://127.0.0.1:8000/docs`
- ReDoc → `http://127.0.0.1:8000/redoc`

## 🛠 Tech Stack

- **FastAPI** – Web framework
- **Pydantic** – Data validation
- **SQLAlchemy** – ORM (planned)
- **Alembic** – Migrations (planned)
- **Uvicorn** – ASGI server

## 🎯 Goal

The main goal of this project is to **learn FastAPI in depth** by building a production-grade template that can later be adapted for real-world applications.
