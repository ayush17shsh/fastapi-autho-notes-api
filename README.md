FastAPI Backend API — JWT Authentication & Architecture

A production-ready REST API built with FastAPI (Python) featuring JWT authentication, secure password hashing, clean project structure, and modern backend best practices. This project is designed as a real-world backend service suitable for learning, portfolios, and production use.

⸻

Features
	•	User Registration & Login
	•	JWT Authentication (Access + Refresh Tokens)
	•	Secure Password Hashing (Argon2 / Bcrypt)
	•	Protected Endpoints
	•	Dependency Injection
	•	Clean Project Structure
	•	SQL Database Integration (PostgreSQL / MySQL / SQLite)
	•	SQLAlchemy ORM
	•	Alembic Migrations
	•	Swagger (OpenAPI) Documentation

⸻

Tech Stack
	•	Python 3.10+
	•	FastAPI
	•	SQLAlchemy
	•	Alembic
	•	Pydantic
	•	JWT (python-jose)
	•	Uvicorn
	•	PostgreSQL / MySQL / SQLite

⸻

Authentication Flow

Visual Flow Diagram

Client → Login API → JWT Issued → Token Stored
      ↓
Protected Request → Token Sent → JWT Validation → User Loaded → Access Granted

Register → Login → Generate JWT → Client stores token →
Send token with each request → Server validates → Access granted


⸻

API Endpoints

Auth

Method	Endpoint	Description
POST	/auth/register	Register new user
POST	/auth/login	Login and receive JWT
POST	/auth/refresh	Refresh access token

User

Method	Endpoint	Access
GET	/users/me	Authenticated


⸻

Security Implementation
	•	JWT-based stateless authentication
	•	Password hashing using Argon2 / Bcrypt
	•	Token-based request authorization
	•	Protected routes using FastAPI dependencies

⸻

⚙️ Setup Instructions

1️⃣ Clone Repository

git clone <repo-url>
cd project

2️⃣ Create Virtual Environment

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate   # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create .env file:

DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


⸻

5️⃣ Run Server

uvicorn app.main:app --reload

⸻

🧠 Project Structure

🏗 Architecture Overview

        Client
           ↓
        FastAPI
           ↓
    ┌──────────────┐
    │   Routers    │
    └──────────────┘
           ↓
    ┌──────────────┐
    │  Services    │
    └──────────────┘
           ↓
    ┌──────────────┐
    │ Repositories │
    └──────────────┘
           ↓
        Database

📁 Folder Structure



app/
├── main.py
├── core/
│    ├── config.py
│    └── security.py
├── api/
│    ├── routes
│    └── deps.py
├── models/
├── schemas/
├── services/
└── db/

---

## 🧪 Sample Request

### Login
```json
POST /auth/login
{
  "email": "test@mail.com",
  "password": "123456"
}

Response:

{
  "access_token": "<jwt>",
  "token_type": "bearer"
}


⸻

💡 Future Improvements
	•	Role-based authorization
	•	Email verification
	•	OAuth login (Google / GitHub)
	•	Docker deployment
	•	Redis caching
	•	Rate limiting

⸻

👨‍💻 Author

Ayush
Backend Developer | Python | FastAPI | Java | Spring Boot

⸻

⭐ If you like this project

Give it a ⭐ on GitHub — it motivates me to build more!
