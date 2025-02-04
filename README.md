# Household Services Backend

This is the backend implementation for the Household Services Application, built with Flask, SQLite, Redis, and Celery.
Note:Single Admin hardcoded
Admin@example.com
Admin@123

admin cant register just login with this cridentials 
## Prerequisites

- Python 3.8+
- Redis Server 6.0+
- SQLite 3.30+
- Postman (for testing)

## Detailed Setup Instructions

### 1. System Setup

#### Install Redis (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Install Redis (macOS)
```bash
brew install redis
brew services start redis
redis-server   
```

#### Install Redis (Windows)
Download and install from Redis website or use WSL2

### 2. Python Environment Setup

Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration Setup

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Update `.env` with your settings:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
REDIS_URL=redis://localhost:6379
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 4. Database Setup

Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 5. Redis Setup

Verify Redis is running:
```bash
redis-cli ping
```
Should return: `PONG`

### 6. Application Launch

Start the Flask application:
```bash
flask run
```

## Project Structure

```
household_services/
├── app.py              # Application entry point
├── config.py           # Configuration settings
├── models.py           # Database models
├── routes/
│   ├── __init__.py
│   ├── admin.py       # Admin endpoints
│   ├── auth.py        # Authentication
│   ├── customer.py    # Customer endpoints
│   ├── professional.py # Professional endpoints
│   └── service.py     # Service endpoints
```

## Security Features

### Authentication
- JWT tokens with 1-hour expiration
- Role-based access control
- Password hashing with bcrypt

### Data Protection
- Password hashing with bcrypt
- Input sanitization
- Rate limiting
- SQL injection protection

## Testing

Run tests:
```bash
python -m pytest tests/
```

For detailed API testing instructions, refer to POSTMAN_TESTING.md