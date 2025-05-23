# SnakeOS Backend

A FastAPI-based backend service for system monitoring and management with secure authentication, designed for Linux systems.

## Features

### Authentication System
- Secure user registration and login
- JWT-based authentication
- Session management
- Protected routes

### System Monitoring
- **CPU Information**
  - Physical and logical cores count
  - CPU frequency (current, min, max)
  - Per-core and total CPU usage

- **Memory Information**
  - RAM usage (total, available, used)
  - Swap memory statistics
  - Memory usage percentages

- **Disk Information**
  - Partition details
  - Storage usage statistics
  - Filesystem information

- **Network Information**
  - Network interfaces
  - IO statistics
  - Network addresses and configurations

- **Platform Information**
  - Linux distribution details
  - System version
  - Boot time
  - Distribution-specific information

## Technology Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with Tortoise ORM
- **Authentication**: JWT (JSON Web Tokens)
- **System Monitoring**: psutil
- **Container**: Docker

## Prerequisites

- Python 3.10+
- PostgreSQL
- Docker and Docker Compose (optional)
- Linux operating system

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SnakeOS-backend.git
cd SnakeOS-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
poetry install
```

4. Set up environment variables (create `.env` file):
```env
# API Settings
PROJECT_NAME="SnakeOS API"
API_V1_STR="/api/v1"

# Database Settings
POSTGRES_USER=snakeos
POSTGRES_PASSWORD=snakeos
POSTGRES_DB=snakeos
POSTGRES_SERVER=db
POSTGRES_PORT=5432

# JWT Settings
SECRET_KEY=your-super-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running with Docker

1. Build and start the services:
```bash
docker compose up -d
```

2. The API will be available at `http://localhost:8000`
3. API documentation at `http://localhost:8000/docs`

## Running Locally

1. Start PostgreSQL server
2. Update `.env` with your database credentials
3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `GET /api/v1/auth/me` - Get current user info

### System Monitoring
- `GET /api/v1/system` - Get complete system information
- `GET /api/v1/system/cpu` - Get CPU information
- `GET /api/v1/system/memory` - Get memory information
- `GET /api/v1/system/disk` - Get disk information
- `GET /api/v1/system/network` - Get network information

## Project Structure

```
app/
├── auth/               # Authentication related code
│   ├── router.py      # Auth endpoints
│   ├── schemas.py     # Auth Pydantic models
│   └── utils.py       # Auth utilities
├── models/            # Database models
│   ├── base.py       # Base model class
│   └── user.py       # User and Session models
├── system/            # System monitoring
│   ├── router.py     # System endpoints
│   ├── schemas.py    # System Pydantic models
│   └── utils/
│       └── system_monitor.py  # System monitoring logic
└── main.py           # Application entry point
```

## Security

- All system monitoring endpoints are protected and require authentication
- Passwords are hashed using secure algorithms
- JWT tokens are used for session management
- Database credentials and secrets are managed through environment variables

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details 