# Expense Tracker API

## Tech Stack
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL (SQLite for local dev)
- JWT Auth (password hashing with bcrypt)

## Setup
1. Create virtualenv and install deps:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Environment variables (optional):
- `DATABASE_URL` (e.g. `postgresql+psycopg2://user:pass@localhost:5432/expenses`)
- `JWT_SECRET_KEY` (default: change-me-in-prod)

3. Run DB migrations:
```bash
alembic upgrade head
```
If you use SQLite locally, a `expense_tracker.db` file will be created.

## Run the API
```bash
uvicorn app.main:app --reload
```
Open `http://localhost:8000`.

## Auth Flow
- `POST /auth/register` { username, email, password } → returns JWT
- `POST /auth/login` { username, password } → returns JWT
Use `Authorization: Bearer <token>` for protected endpoints.

## Endpoints
- Users: `GET /users/me`, `PUT /users/me`
- Expenses: `GET/POST /expenses`, `GET/PUT/DELETE /expenses/{id}`
- Categories: `GET/POST /categories`, `PUT/DELETE /categories/{id}`
- Reports: `GET /reports/summary`

## CSV Import
```bash
python -m scripts.import_csv path/to/file.csv username
```
CSV columns: amount,currency,category,description,date (YYYY-MM-DD)

## Docker
```bash
docker compose up --build
```
The API will be at `http://localhost:8000` and Postgres at `localhost:5432`.
