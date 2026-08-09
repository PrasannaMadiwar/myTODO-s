 
# myTODO-s

A FastAPI-based TODO application with user authentication, task management, and scheduled email reminders.

## Features

- User registration and login
- JWT-based authentication
- Create TODO reminders
- One-time, daily, weekly, and monthly reminders
- Email notifications using Resend
- SQLite database storage
- Pagination and search for TODO items
- Update and delete TODOs

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT authentication with `python-jose`
- Password hashing with `passlib` and `bcrypt`
- APScheduler
- Resend email API

## Project Structure

``` 
myTODO-s/
├── apps/
│   └── api/
│       ├── databases/
│       │   ├── todo.db
│       │   └── jobs.sqlite
│       ├── pydantic_schemas/
│       │   ├── schemas.py
│       │   └── response_schemas.py
│       ├── services/
│       │   ├── auth.py
│       │   ├── background_tasks.py
│       │   ├── mail_service.py
│       │   └── models.py
│       └── source/
│           ├── configuration.py
│           ├── dependecies.py
│           └── main.py
├── .env.example
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd myTODO-s
```

### 2. Create and activate a virtual environment

```bash
python -m venv env
```

On Windows:

```bash
env\Scripts\activate
```

On macOS/Linux:

```bash
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `dotenv` is missing, also install:

```bash
pip install python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECURITY_KEY="your_secret_key_here"
ALGORITHM="HS256"
RESEND_API_KEY="your_resend_api_key_here"
```

## Running the App

```bash
uvicorn apps.api.source.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Home

```http
GET /
```

Returns a welcome message.

### Create User

```http
POST /create_user
```

Request body:

```json
{
  "username": "john",
  "password": "password123",
  "user_email": "john@example.com"
}
```

### Login

```http
POST /login
```

Uses OAuth2 form data:

```text
username=john
password=password123
```

Returns a bearer token.

### Create One-Time TODO

```http
POST /create_todo_once
```

Requires bearer token.

```json
{
  "title": "Submit assignment",
  "time": "2026-08-10T09:00:00",
  "is_completed": false
}
```

### Create Daily TODO

```http
POST /create_todo_daily
```

### Create Weekly TODO

```http
POST /create_todo_weekly
```

### Create Monthly TODO

```http
POST /create_todo_monthly
```

### Get TODOs

```http
GET /get_todos/{page_no}?page_size=10
```

### Search TODOs

```http
GET /search_todo/{todo_name}
```

### Update TODO Status

```http
PUT /update_todo_status/{todo_id}?is_completed=true
```

### Update TODO

```http
PUT /update_todo/{todo_id}
```

Request body:

```json
{
  "title": "Updated task",
  "time": "2026-08-10T10:00:00",
  "is_completed": false
}
```

### Delete TODO

```http
DELETE /delete_todo/{todo_id}
```

## Authentication

Protected routes require an access token from `/login`.

Use the token as:

```http
Authorization: Bearer <access_token>
```

## Notes

- TODO data is stored in `apps/api/databases/todo.db`.
- Scheduled jobs are stored in `apps/api/databases/jobs.sqlite`.
- Email reminders are sent through Resend.
- Scheduler timezone is set to `Asia/Kolkata`.
```
