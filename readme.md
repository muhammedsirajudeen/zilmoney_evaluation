```markdown
# ZilMoney Evaluation API

A **FastAPI** application for managing users, expenses, and budgets, built with **async SQLAlchemy**, **PostgreSQL**, **Alembic migrations**, and **JWT authentication**.

---

## Features

- **User Management**
  - Create users with `username` and optional `salary`.
  - Returns a **JWT access token** on user creation.

- **Expense Management**
  - Create expenses for users with `name`, `amount`, `category`.
  - Filter expenses by day, week, month, or category.

- **Budget Summary**
  - Total expenses, total salary, remaining amount.
  - Category-wise breakdown.

- **Authentication**
  - JWT-based authentication.
  - Async endpoints for better performance.

- **Database**
  - PostgreSQL with **asyncpg**.
  - Managed with **SQLAlchemy ORM** and **Alembic migrations**.

---

## Tech Stack

- Python 3.12+  
- FastAPI  
- SQLAlchemy (async)  
- PostgreSQL + asyncpg  
- Alembic (migrations)  
- PyJWT (JWT tokens)  
- Pydantic (request/response schemas)

---

## Project Structure

```

zilmoney/
├── alembic/                  # Alembic migrations
│   ├── versions/
│   └── env.py
├── config/
│   └── database.py           # Async SQLAlchemy engine & session
├── models/
│   └── hello.py              # User and Expense models
├── routes/
│   └── hello.py              # API endpoints
├── schemas/
│   └── schemas.py            # Pydantic schemas
├── auth.py                   # JWT helpers (create/decode)
├── main.py                   # FastAPI app
├── requirements.txt
├── .gitignore
└── README.md

````

---

## Setup & Installation

1. **Clone the repo**

```bash
git clone <repo_url>
cd zilmoney
````

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Setup PostgreSQL**

* Create a database:

```sql
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

* Update `config/database.py` with your DB credentials.

5. **Run Alembic migrations**

```bash
alembic upgrade head
```

6. **Run FastAPI server**

```bash
uvicorn main:app --reload
```

Server will start at: `http://127.0.0.1:8000`

---

## API Endpoints

### User Endpoints

* **POST /api/users/** — Create a new user and get JWT token

**Body:**

```json
{
  "username": "sirajudeen",
  "salary": 50000
}
```

**Response:** User details + JWT token

---

### Expense Endpoints

* **POST /api/expenses/** — Create an expense

**Body:**

```json
{
  "user_id": 1,
  "name": "Lunch",
  "amount": 100,
  "category": "Food"
}
```

* **GET /api/expenses/{user\_id}** — List user expenses

**Query Params (optional):**

* `day=YYYY-MM-DD`
* `week=WW&year=YYYY`
* `month=MM&year=YYYY`
* `category=Food`

---

### Budget Summary

* **GET /api/totals/{user\_id}** — Get user budget summary

**Response:**

```json
{
  "total_expense": 500,
  "total_salary": 5000,
  "remaining_amount": 4500,
  "category_breakdown": {
    "Food": 200,
    "Transport": 100,
    "Utilities": 200
  }
}
```

---

### Authentication

* JWT is returned on user creation.
* Use `Authorization: Bearer <JWT>` header for protected routes.

---

## Notes

* Invalid enum values for categories return **400 Bad Request**.
* All endpoints are **async** for better performance.
* Alembic manages database migrations, including enum changes.

---

## Gitignore

Make sure your project ignores unnecessary files:

```gitignore
__pycache__/
*.py[cod]
*$py.class
*.so
build/
dist/
*.egg-info/
venv/
.env/
.vscode/
.idea/
*.log
*.sqlite3
uploads/
tmp/
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/
```

---

### License

MIT License

```

---

