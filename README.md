# SpyNet Backend API

A FastAPI backend service for the SpyNet project, supporting a Detective Mobile App and a Manager Dashboard Web App.

## Features

- 🔐 **Authentication**: Sign up, sign in with Supabase Auth and JWT tokens
- 👥 **User Management**: Role-based access control (detective, manager)
- 📋 **Case Management**: Create, read, update, and delete cases with role-based permissions
- 🔒 **Security**: JWT token verification on all protected endpoints
- 🌐 **CORS**: Configured for multiple frontend origins
- 📚 **OpenAPI Docs**: Interactive API documentation at `/docs`

## Tech Stack

- **Framework**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth
- **Deployment**: Render

## Project Structure

```
spynet-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration settings
│   ├── middleware.py        # JWT authentication middleware
│   ├── models/              # Pydantic models
│   │   ├── user.py
│   │   └── case.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── cases.py
│   ├── services/            # Business logic
│   │   ├── supabase_service.py
│   │   └── auth_service.py
│   └── utils/               # Utilities
│       └── permissions.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd spynet-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Supabase

1. Create a new project at [Supabase](https://supabase.com)
2. Go to Project Settings → API to get your credentials
3. Create the required tables:

#### Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY REFERENCES auth.users(id),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('detective', 'manager')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Cases Table

```sql
CREATE TABLE cases (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    details TEXT NOT NULL,
    location TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'closed')),
    detective_id UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_cases_detective_id ON cases(detective_id);
CREATE INDEX idx_cases_status ON cases(status);
```

### 5. Environment Variables

1. Copy `.env.example` to `.env`
2. Fill in your Supabase credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

## Running Locally

### Development Mode

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /auth/signup` - Create new user
- `POST /auth/login` - Login user and get JWT token

### Users

- `GET /users` - List all users (manager only)
- `GET /users/{id}` - Get user details
- `PUT /users/{id}` - Update user (manager can update any, users can update own)

### Cases

- `GET /cases` - List cases (all cases for managers, own cases for detectives)
- `GET /cases/{id}` - Get case details
- `POST /cases` - Create new case (manager only)
- `PUT /cases/{id}` - Update case (detectives can update own cases)
- `DELETE /cases/{id}` - Delete case (manager only)

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Example Request

```bash
curl -X GET "http://localhost:8000/users" \
  -H "Authorization: Bearer your-jwt-token-here"
```

## Role-Based Access Control

### Detective
- View own assigned cases
- Update status and details of own cases
- Update own profile name
- View own profile

### Manager
- View all cases
- Create cases
- Assign cases to detectives
- Delete cases
- View and manage all users
- Update any user profile

## Deployment on Render

### 1. Connect Repository

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Select the repository

### 2. Configuration

- **Name**: `spynet-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Environment Variables

In Render dashboard, add these environment variables:

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
CORS_ORIGINS=https://your-frontend-domain.com
```

### 4. Deploy

Click "Create Web Service" to deploy. Your API will be available at `https://your-service.onrender.com`

## Testing

### Sign Up Example

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "detective@example.com",
    "password": "securepassword123",
    "name": "John Detective",
    "role": "detective"
  }'
```

### Login Example

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "detective@example.com",
    "password": "securepassword123"
  }'
```

### Get Cases Example

```bash
curl -X GET "http://localhost:8000/cases" \
  -H "Authorization: Bearer your-jwt-token"
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `201` - Created
- `204` - No Content (successful deletion)
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
