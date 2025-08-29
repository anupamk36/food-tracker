# 🍽️ Food Nutrition Tracker

A full-stack web application that allows users to upload images of meals, automatically extracts food items and their nutritional information using the **OpenAI API**, and visualizes dietary data (calories, protein, carbs, fats) with a modern dashboard.

This project is designed to demonstrate:

- **FastAPI** backend with JWT-based auth and PostgreSQL persistence.
- **React + Vite** frontend styled with **Tailwind CSS**, featuring charts powered by **Recharts**.
- Integration with the **OpenAI Chat Completions API** to parse meal images into structured JSON (items + nutrition).
- Containerized deployment with **Docker Compose** (services: `fn_backend`, `fn_frontend`, `fn_db`).

---

## 🏗️ Project Architecture

           ┌────────────────────────┐
           │        Frontend        │
           │   React + Vite +       │
           │   Tailwind + Recharts  │
           └──────────┬─────────────┘
                      │ (REST, JSON)
                      ▼
           ┌────────────────────────┐
           │        Backend         │
           │ FastAPI + SQLAlchemy   │
           │ JWT Auth, CRUD,        │
           │ OpenAI integration     │
           └──────────┬─────────────┘
                      │ (SQL, JSONB)
                      ▼
           ┌────────────────────────┐
           │        Database        │
           │   PostgreSQL (meals,   │
           │   users, auth, etc.)   │
           └────────────────────────┘

### Data Flow

1. **Upload Meal**  
   - User logs in and uploads an image (`/api/meals/`).
   - FastAPI saves the image to `/uploads/` and inserts a new row in `meals` with `status = "pending"`.

2. **Background Analysis**  
   - A FastAPI background task calls the **OpenAI API**, sending the uploaded image path + instructions.
   - The model responds with JSON describing `items` and `nutrition` (calories, protein, carbs, fat).
   - The backend parses this JSON robustly and updates the same row with structured data (`JSONB`) and sets `status = "done"`.

3. **Dashboard Visualization**  
   - Frontend fetches `/api/meals/` and `/api/meals/stats`.
   - Data is visualized via charts:
     - **Calories over time** with moving average and goal line.
     - **Stacked macros** by day.
     - **Macro split donut** (last 7 days).
     - **Top items** bar chart.
   - Each meal card shows timestamp, image, items + servings, and nutrition badges.

---

## 🧰 Technologies Used

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — async Python web framework.
- **[SQLAlchemy](https://www.sqlalchemy.org/)** ORM with Postgres dialects.
- **PostgreSQL** — relational DB storing `users` and `meals` (with JSONB for items/nutrition).
- **JWT (JSON Web Tokens)** via `python-jose` — secure user authentication.
- **Pydantic** — request/response data validation.
- **OpenAI API** — nutrition extraction from meal images.
- **Docker** — containerized backend + DB.

### Frontend
- **React 18/19** — UI framework.
- **Vite** — fast dev/build tool.
- **Tailwind CSS 4** — utility-first styling.
- **Recharts** — charting/visualizations.
- **Axios** — HTTP client for API calls.
- **React Router DOM** — client-side routing.

---

## 📂 Database Schema (simplified)

### `users`
| column     | type     |
|------------|----------|
| id         | int PK   |
| email      | text     |
| password   | hashed   |

### `meals`
| column     | type       | notes |
|------------|------------|-------|
| id         | int PK     |       |
| owner_id   | int (FK)   | references users.id |
| image_path | text       | `/uploads/<uuid>.jpg` |
| status     | text       | `pending` / `done` / `failed` |
| timestamp  | timestamptz| default `now()` |
| items      | JSONB      | `[{"name":"Salmon","serving":"150g"}, ...]` |
| nutrition  | JSONB      | `{"calories":650,"protein_g":45,"carbs_g":60,"fat_g":18}` |
| notes      | text       | optional user notes |

---
