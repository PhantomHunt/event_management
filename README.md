🧪 Mini Event Management System API
A clean-architecture-based FastAPI backend for managing events and attendees, featuring:

✅ Async SQLAlchemy (PostgreSQL)

✅ IST timezone support

✅ Duplicate & overbooking protection

✅ Pagination on attendee lists

✅ Swagger documentation

✅ Pytest for unit testing

📦 Tech Stack
FastAPI (async API framework)

PostgreSQL (real DB)

SQLAlchemy [async] (ORM)

Pydantic (input validation)

Uvicorn (ASGI server)

Pytest (unit testing)

🚀 Features
Create, list, and register events

Prevent overbooking and duplicate registrations

Attendee listing with pagination

Timezone-aware scheduling (IST, auto-convert)

Swagger/OpenAPI documentation (/docs)

⚙️ Local Setup (macOS/Linux/WSL)
1. ✅ Clone the Repository
git clone https://github.com/your-username/event-management-api.git
cd event-management-api
2. ✅ Setup Python Virtual Environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. ✅ Setup PostgreSQL Locally
Install via Homebrew:
brew install postgresql
brew services start postgresql
Create DB and user:

psql postgres
# Inside the psql shell:
CREATE DATABASE events_db;
CREATE USER event_user WITH PASSWORD 'event_pass';
GRANT ALL PRIVILEGES ON DATABASE events_db TO event_user;
\q
4. ✅ Setup Environment Variables
Create .env file:


DATABASE_URL=postgresql+asyncpg://event_user:event_pass@localhost/events_db
TZ=Asia/Kolkata
5. ✅ Run the Application

uvicorn app.main:app --reload
Open http://localhost:8000/docs for interactive Swagger UI.

🧪 Running Tests

pytest
Unit tests are located in the /tests folder and cover key endpoints.

📘 API Endpoints
Method	Endpoint	Description
POST	/events	Create a new event
GET	/events	List all upcoming events
POST	/events/{event_id}/register	Register attendee (prevents overbooking and duplicate emails)
GET	/events/{event_id}/attendees	Get attendees (supports pagination)

🕒 Timezone Support
All datetime inputs are stored in IST (Asia/Kolkata). When queried or created in other timezones, the system adjusts slots accordingly using pytz.

