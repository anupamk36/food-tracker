# Food Nutrition App

## Local dev (docker-compose)
1. Copy `backend/.env.example` -> `backend/.env`, fill `JWT_SECRET` and `OPENAI_API_KEY` if available.
2. docker compose up --build
3. Frontend: http://localhost:3000  Backend API: http://localhost:8000

## Production notes
- Use managed Postgres (RDS) and S3 for images.
- Replace background tasks with Celery or RQ for reliability.
- Use HTTPS, rotate JWT_SECRET, use strong secrets and monitoring.
