# Online Course Management System

A comprehensive, enterprise-grade course management platform built with Django and Django REST Framework, following SOLID principles and clean architecture patterns.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [User Roles & Permissions](#user-roles--permissions)
- [Project Structure](#project-structure)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Contributing](#contributing)

## Features

### Authentication & Authorization
- **JWT-based authentication** with access and refresh tokens
- **Token blacklisting** for secure logout
- **Role-based access control** (Teachers and Students)
- **Secure password validation** with Django's built-in validators

### User Management
- **Custom user model** with email-based authentication
- **Role assignment** (Teacher/Student)
- **User registration and profile management**
- **Grouped user listing** by role

### Course Management
- **Full CRUD operations** for courses
- **Teacher-owned courses** with primary ownership model
- **Many-to-many relationships** for teachers and students
- **Course enrollment system**
- **Unique course names** per teacher constraint
- **Atomic transactions** for data consistency

### Enterprise Architecture
- **SOLID principles** implementation
- **Service layer pattern** with dependency injection
- **DTO (Data Transfer Objects)** for clean data flow
- **Interface segregation** for better maintainability
- **Comprehensive validation** with custom validators
- **N+1 query optimization** with select_related

## Technology Stack

### Backend
- **Django 5.2.5** - Web framework
- **Django REST Framework 3.16.1** - API framework
- **Django REST Framework SimpleJWT 5.5.1** - JWT authentication
- **PostgreSQL** - Production database (SQLite for development)
- **Python 3.11+** - Programming language

### Architecture Patterns
- **Clean Architecture** - Separation of concerns
- **Service Layer Pattern** - Business logic isolation
- **Repository Pattern** - Data access abstraction
- **DTO Pattern** - Data transfer standardization
- **Pipeline Pattern** - Validation orchestration

### Code Quality
- **SOLID Principles** - Object-oriented design
- **Type Hints** - Enhanced code readability
- **Enum-based Constants** - Eliminates magic strings
- **Dataclasses** - Immutable data structures

## Architecture

### Layer Structure
```
┌─────────────────────────────────────┐
│           API Layer (Views)         │ ← HTTP Request/Response
├─────────────────────────────────────┤
│        Serialization Layer         │ ← Data Validation & Serialization
├─────────────────────────────────────┤
│          Service Layer              │ ← Business Logic
├─────────────────────────────────────┤
│         Validation Layer            │ ← Business Rules & Data Validation
├─────────────────────────────────────┤
│           Data Layer               │ ← Models & Database Access
└─────────────────────────────────────┘
```

### Core Principles
- **Single Responsibility** - Each class has one reason to change
- **Open/Closed** - Open for extension, closed for modification
- **Liskov Substitution** - Objects are replaceable with their subtypes
- **Interface Segregation** - Many specific interfaces over one general
- **Dependency Inversion** - Depend on abstractions, not concretions

## Installation

### Prerequisites
- Python 3.11 or higher
- uv (recommended) or pip
- PostgreSQL (for production)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd online-course-management-system
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment variables**
   Create a `.env` file in the project root:
   ```env
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=1
   DATABASE_URL=sqlite:///db.sqlite3  # or PostgreSQL URL for production
   ```

4. **Database setup**
   ```bash
   uv run python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   uv run python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## Configuration

### Database Configuration

**Development (SQLite)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Production (PostgreSQL)**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'course_management',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### JWT Configuration
```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(minutes=60),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "teacher"  // or "student"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

#### Token Refresh
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "your-refresh-token"
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "refresh": "your-refresh-token"
}
```

### User Endpoints

#### List Users (Grouped by Role)
```http
GET /api/users/
Authorization: Bearer your-access-token
```

**Response:**
```json
{
  "teacher": [
    {
      "id": 1,
      "email": "teacher@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "role": "teacher"
    }
  ],
  "student": [
    {
      "id": 2,
      "email": "student@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "student"
    }
  ]
}
```

### Course Endpoints

#### List Courses
```http
GET /api/courses/
Authorization: Bearer your-access-token
```

#### Create Course
```http
POST /api/courses/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "name": "Introduction to Python",
  "description": "Learn Python programming fundamentals",
  "teacher_ids": [2, 3],    // Optional: Additional teachers
  "student_ids": [4, 5, 6]  // Optional: Enrolled students
}
```

#### Retrieve Course
```http
GET /api/courses/{id}/
Authorization: Bearer your-access-token
```

#### Update Course (Full)
```http
PUT /api/courses/{id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "name": "Advanced Python",
  "description": "Advanced Python concepts and frameworks",
  "primary_owner_id": 1,    // Optional: Change owner
  "teacher_ids": [2, 3, 4], // Optional: Update teachers
  "student_ids": [5, 6, 7]  // Optional: Update students
}
```

#### Update Course (Partial)
```http
PATCH /api/courses/{id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "name": "Updated Course Name"
  // Only provided fields will be updated
}
```

#### Delete Course
```http
DELETE /api/courses/{id}/
Authorization: Bearer your-access-token
```

### Response Formats

#### Success Response
```json
{
  "id": 1,
  "name": "Course Name",
  "description": "Course description",
  "primary_owner": {
    "id": 1,
    "email": "teacher@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "role": "teacher"
  },
  "teacher_count": 2,
  "student_count": 5
}
```

#### Error Response
```json
{
  "errors": [
    "Course name cannot be empty",
    "User must be teacher"
  ]
}
```

## User Roles & Permissions

### Teacher Role
- Create courses (becomes primary owner)
- Update/delete their own courses
- Manage teachers and students in their courses
- View all courses
- Cannot modify courses owned by other teachers

### Student Role
- View all courses
- Be enrolled in courses by teachers
- Cannot create, update, or delete courses
- Cannot manage course memberships

### Permission Matrix

| Action | Teacher (Owner) | Teacher (Non-owner) | Student |
|--------|----------------|-------------------|---------|
| Create Course | Yes | Yes | No |
| View Courses | Yes | Yes | Yes |
| Update Own Course | Yes | No | No |
| Delete Own Course | Yes | No | No |
| Manage Course Members | Yes | No | No |

## Project Structure

```
online-course-management-system/
├── apps/
│   ├── courses/                    # Course management app
│   │   ├── models.py              # Course, CourseTeacher, CourseStudent models
│   │   ├── views.py               # CourseViewSet (CRUD operations)
│   │   ├── serializers.py         # API serializers
│   │   ├── permissions.py         # IsCoursePrimaryOwner permission
│   │   ├── admin.py               # Django admin configuration
│   │   ├── services/              # Service layer (business logic)
│   │   │   ├── course.py          # CourseCreationService, CourseUpdateService
│   │   │   ├── user.py            # UserService
│   │   │   ├── relationship_manager.py # Course relationship management
│   │   │   ├── dtos/              # Data Transfer Objects
│   │   │   │   ├── course.py      # Course-related DTOs
│   │   │   │   └── user.py        # User-related DTOs
│   │   │   └── validation/        # Validation layer
│   │   │       ├── base.py        # Base validator with shared logic
│   │   │       ├── creation.py    # Course creation validation
│   │   │       ├── update.py      # Course update validation
│   │   │       ├── user_role.py   # User role validation
│   │   │       ├── uniqueness.py  # Uniqueness validation
│   │   │       ├── business_rules.py # Business rule validation
│   │   │       └── interfaces.py  # Validation interfaces
│   │   └── migrations/            # Database migrations
│   └── users/                     # User management app
│       ├── models.py              # Custom User model
│       ├── views/                 # Authentication and user views
│       │   ├── auth.py            # RegisterView, LoginView, LogoutView
│       │   └── user.py            # UserViewSet
│       ├── serializers/           # User serializers
│       │   ├── auth.py            # Authentication serializers
│       │   └── user.py            # User serializers
│       ├── services/              # User services
│       │   ├── registration.py    # User registration service
│       │   ├── authentication.py  # Login service
│       │   ├── logout.py          # Logout service
│       │   ├── token_blacklist.py # Token management
│       │   └── user_service.py    # User business logic
│       ├── permissions/           # User permissions
│       │   └── blacklist.py       # Token blacklist permission
│       └── migrations/            # Database migrations
├── common/
│   └── enums.py                   # Centralized enums and constants
├── config/                        # Django configuration
│   ├── settings.py                # Django settings
│   ├── urls.py                    # URL configuration
│   ├── wsgi.py                    # WSGI configuration
│   └── asgi.py                    # ASGI configuration
├── manage.py                      # Django management script
├── pyproject.toml                 # Project dependencies and metadata
└── README.md                      # This file
```

## Development Guidelines

### Code Style
- Follow **PEP 8** Python style guide
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all classes and methods
- Use **enums** instead of magic strings/numbers

### Architecture Principles
1. **Service Layer Pattern**: Business logic in services, not views
2. **DTO Pattern**: Use immutable dataclasses for data transfer
3. **Dependency Injection**: Inject dependencies via constructor parameters
4. **Interface Segregation**: Create focused, single-purpose interfaces
5. **Validation Pipeline**: Use pipeline pattern for complex validation

### Example Service Implementation
```python
@dataclass
class CourseCreationService:
    validation_service: CourseCreationValidatorInterface = field(default_factory=CourseCreationValidator)
    relationship_manager: CourseRelationshipManagerInterface = field(default_factory=CourseRelationshipManager)

    def create_course(self, request: CourseCreationRequest) -> Course:
        validation_result = self.validation_service.validate_course_creation(request)
        
        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)
        
        return self._create_course_with_relationships(request, validation_result)
```

### Database Optimization
- Use `select_related()` for foreign key relationships
- Use `prefetch_related()` for many-to-many relationships
- Implement custom QuerySets with `annotate()` for aggregations
- Use database constraints for data integrity


### Code Review Checklist
- [ ] SOLID principles followed
- [ ] No magic strings/numbers (use enums)
- [ ] Proper error handling
- [ ] Type hints included
- [ ] Tests written and passing
- [ ] Documentation updated

