# Leverage

A modern financial technology (FinTech) application built with FastAPI that provides digital banking and peer-to-peer payment services.

## 🚀 Features

### User Management
- User registration and authentication
- Profile management with image uploads
- Role-based access control (user/admin)
- KYC-style verification system (verified/pending/unverified)

### Financial Services
- **Digital Accounts**: Each user gets an account with balance tracking
- **Leverage Tags**: Unique usernames for P2P transfers (like $cashtags)
- **Transaction Types**: Deposits, withdrawals, transfers, card payments, charges
- **Account Statuses**: Active, dormant, blocked

### Transaction System
- P2P transfers using leverage tags
- Balance management with decimal precision
- Transaction history and ledger tracking
- Insufficient funds validation

## 🛠 Technology Stack

- **Backend**: FastAPI with Python 3.13.8
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt password hashing
- **Infrastructure**: Docker containers with docker-compose
- **Additional**: Cloudinary for image storage, phpMyAdmin for database management

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.13.8 (for local development)
- MySQL client (optional, for direct database access)

## 🚀 Quick Start

### Using Docker Compose (Recommended)

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
   - API Documentation: http://localhost:8000/docs
   - Database Admin (phpMyAdmin): http://localhost:8080

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Ensure MySQL is running and configured
   # Run database migrations
   alembic upgrade head
   ```

3. **Start the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /leverage/users` | User registration |
| `POST /leverage/tags/users` | Create leverage tag |
| `POST /leverage/accounts` | P2P transfers |
| `POST /leverage/auth/login` | User authentication |
| `GET /leverage/verification` | User verification status |

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

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

## 🏗 Project Structure

```
leverage/
├── app/
│   ├── models/           # SQLAlchemy models
│   ├── routes/           # API route handlers
│   ├── schemas/          # Pydantic models
│   ├── database/         # Database configuration
│   ├── auth/             # Authentication utilities
│   ├── middlewares/      # Custom middlewares
│   ├── alembic/          # Database migrations
│   └── main.py           # FastAPI application entry
├── docker-compose.yml    # Docker orchestration
├── Dockerfile           # Container configuration
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt with 12 rounds for password security
- **User Verification**: KYC-style verification system
- **Input Validation**: Comprehensive input sanitization
- **Account Status**: Account status validation for transactions

## 💡 Core Concepts

### Leverage Tags
Leverage tags are unique usernames that allow users to send money easily without needing account numbers. Similar to $cashtags on other platforms.

### Account Types
- **Regular Account Balance**: Traditional banking balance
- **Leverage Balance**: Special balance for leverage-specific transactions

### Verification Levels
- **Unverified**: Basic access, limited functionality
- **Pending**: Verification submitted, under review
- **Verified**: Full access to all features

## 🧪 Testing

```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

## 📝 Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🚀 Deployment

### Production Deployment

1. **Set up production environment variables**
2. **Configure SSL certificates**
3. **Set up reverse proxy (nginx)**
4. **Configure production database**
5. **Deploy with Docker Compose**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team

## 🎯 Roadmap

- [ ] Mobile application
- [ ] Advanced fraud detection
- [ ] Interest-bearing accounts
- [ ] Investment features
- [ ] Multi-currency support
- [ ] API rate limiting
- [ ] Advanced analytics dashboard

---

**Leverage** - Your gateway to financial freedom. We provide, Leverage!
