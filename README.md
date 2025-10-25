# Contacts API (FastAPI + SQLAlchemy + PostgreSQL)


## Запуск локально
1. Створи БД PostgreSQL, наприклад `contacts_db`.
2. Скопіюй `.env.example` → `.env` і задай `DATABASE_URL`.
3. Встанови залежності:
```bash
python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload