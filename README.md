# Leverage

**Your gateway to financial freedom.** A modern FinTech application providing digital banking and peer-to-peer payment services.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.13.8-3776AB?style=flat&logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql)](https://mysql.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)](https://docker.com)

---

## 🚀 Live Demo

| Resource | URL |
|----------|-----|
| **API** | https://leverage-6elm.onrender.com |
| **Swagger UI** | https://leverage-6elm.onrender.com/docs |
| **ReDoc** | https://leverage-6elm.onrender.com/redoc |

---

## ✨ Features

### User Management
- User registration and authentication
- Profile management with image uploads (Cloudinary)
- Role-based access control (user / admin)
- KYC-style verification system (verified / pending / unverified)

### Financial Services
- **Digital Accounts** — each user gets an account with balance tracking
- **Leverage Tags** — unique usernames for P2P transfers (like $cashtags)
- **Transaction Types** — deposits, withdrawals, transfers, card payments, charges
- **Account Statuses** — active, dormant, blocked

### Transaction System
- P2P transfers using leverage tags
- Balance management with decimal precision
- Transaction history and ledger tracking
- Insufficient funds validation

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI with Python 3.13.8 |
| **Database** | MySQL 8.0 with SQLAlchemy ORM |
| **Authentication** | JWT tokens with bcrypt password hashing (12 rounds) |
| **Infrastructure** | Docker & Docker Compose |
| **Image Storage** | Cloudinary |
| **DB Migrations** | Alembic |

---

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.13.8 (for local development without Docker)
- A MySQL database (local or remote)

---

## 🚀 Quick Start

### Using Docker Compose (Recommended for local development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd leverage
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - phpMyAdmin: http://localhost:8080

---

### Local Development (without Docker)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

4. **Start the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## 📚 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/leverage/users` | User registration |
| `POST` | `/leverage/tags/users` | Create leverage tag |
| `POST` | `/leverage/accounts` | P2P transfers |
| `POST` | `/leverage/auth/login` | User authentication |
| `GET` | `/leverage/verification` | User verification status |

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=leverage_db
FORWARD_DB_PORT=3306

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key
JWT_EXPIRATION_TIME=3600
JWT_ALGORITHM=HS256

# Cloudinary Configuration (for image uploads)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## 🏗 Project Structure

```
leverage/
├── app/
│   ├── alembic/          # Database migrations
│   ├── auth/             # Authentication utilities
│   ├── database/         # Database configuration
│   ├── middlewares/      # Custom middlewares
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # API route handlers
│   ├── schemas/          # Pydantic models
│   ├── enums.py          # Application enums
│   └── main.py           # FastAPI application entry point
├── docker-compose.yml    # Docker orchestration (local development)
├── Dockerfile            # Container configuration
├── requirements.txt      # Python dependencies
├── alembic.ini           # Alembic configuration
├── .env.example          # Environment variables template
└── .gitignore
```

---

## 🔐 Security Features

- **JWT Authentication** — secure token-based authentication with expiration
- **Password Hashing** — bcrypt with 12 rounds
- **User Verification** — KYC-style verification required for transactions
- **Input Validation** — Pydantic schema validation on all inputs
- **Account Status Checks** — blocked/dormant accounts cannot transact

---

## 💡 Core Concepts

### Leverage Tags
Leverage tags are unique usernames that allow users to send money easily without needing account numbers — similar to $cashtags on Cash App.

### Verification Levels
| Level | Access |
|-------|--------|
| **Unverified** | Basic access, limited functionality |
| **Pending** | Verification submitted, under review |
| **Verified** | Full access to all features |

### Account Statuses
| Status | Description |
|--------|-------------|
| **Active** | Normal operation |
| **Dormant** | Inactive account |
| **Blocked** | Suspended, no transactions allowed |

---

## 📝 Database Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Rollback one migration
alembic downgrade -1
```

---

## 🚀 Deployment

### Render (Current production setup)

1. Push your code to GitHub
2. Connect your repo on [render.com](https://render.com)
3. Add all environment variables in the Render dashboard under **Environment**
4. Set **Pre-Deploy Command**:
   ```bash
   alembic upgrade head
   ```
5. Render auto-deploys on every push to your main branch

> **Note:** Render's free tier spins down after 15 minutes of inactivity. The first request after sleep may take 30–50 seconds to respond.

---

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes
   ```bash
   git commit -m "add amazing feature"
   ```
4. Push to the branch
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

---

## 🎯 Roadmap

- [ ] API rate limiting
- [ ] Email notifications on transactions
- [ ] Transaction PIN for extra security
- [ ] Mobile application
- [ ] Multi-currency support
- [ ] Advanced fraud detection
- [ ] Interest-bearing accounts
- [ ] Investment features
- [ ] Analytics dashboard

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**Leverage** — We provide, Leverage!