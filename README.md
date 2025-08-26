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
- [Contributing](#contributing)
- [Testing](#testing)

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
- **Pagination support** for list endpoints

### Lecture Management
- **Nested CRUD operations** for lectures within courses
- **Lecture ownership validation** (course owners and assigned teachers)
- **Topic uniqueness** within each course
- **Comprehensive validation pipeline** with business rules
- **Service layer architecture** following SOLID principles
- **Pagination support** for lecture lists

### Homework Management
- **Nested CRUD operations** for homework assignments within lectures
- **Homework ownership validation** (homework creators, course owners, and assigned teachers)
- **Title uniqueness** within each lecture
- **Due date management** for assignments
- **Comprehensive validation pipeline** with business rules
- **Service layer architecture** following SOLID principles
- **Pagination support** for homework lists

### Homework Submission Management
- **Nested CRUD operations** for submissions within homework assignments
- **Submission ownership validation** (students can manage their own submissions, teachers can view all)
- **One submission per student** per homework constraint
- **Submission status tracking** (draft vs submitted for review)
- **Student enrollment validation** (only enrolled students can submit)
- **Comprehensive validation pipeline** with business rules
- **Service layer architecture** following SOLID principles
- **Pagination support** for submission lists

### Grades & Feedback
- **Grades** for each submission (one grade per submission)
- **Teachers** can create/update/delete grades; students can view their own grades
- **Strict privacy**: unenrolled students cannot access grades (403)
- **Comments on grades** by teacher and the submission’s student
- **Nested endpoints** under submissions

### Enterprise Architecture
- **SOLID principles** implementation
- **Service layer pattern** with dependency injection
- **DTO (Data Transfer Objects)** for clean data flow
- **Interface segregation** for better maintainability
- **Comprehensive validation** with custom validators
- **N+1 query optimization** with select_related
- **Enum-based constants** eliminating magic strings
- **Protocol-based interfaces** for dependency inversion

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

Swagger UI is available by default when the server is running:

- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI JSON: `http://localhost:8000/api/schema/`

The source OpenAPI spec used for reference examples also lives at `docs/openapi.yaml`.

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

#### List Courses (Paginated)
```http
GET /api/courses/?page=1&page_size=10
Authorization: Bearer your-access-token
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/courses/?page=2&page_size=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Introduction to Python",
      "description": "Learn Python programming fundamentals",
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
  ],
  "page_info": {
    "current_page": 1,
    "total_pages": 3,
    "page_size": 10
  }
}
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
  "name": "Advanced Python Programming",
  "description": "Advanced Python concepts and frameworks",
  "primary_owner_id": 1,
  "teacher_ids": [2, 3],
  "student_ids": [4, 5, 6]
}
```

#### Update Course (Partial)
```http
PATCH /api/courses/{id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "name": "Updated Course Name"
}
```

#### Delete Course
```http
DELETE /api/courses/{id}/
Authorization: Bearer your-access-token
```

### Lecture Endpoints

#### List Lectures for a Course (Paginated)
```http
GET /api/courses/{course_id}/lectures/?page=1&page_size=10
Authorization: Bearer your-access-token
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response:**
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/courses/1/lectures/?page=2&page_size=10",
  "previous": null,
  "results": [
    {
      "id": 1,
      "topic": "Introduction to Python Programming",
      "presentation": "python_intro_slides.pdf",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ],
  "page_info": {
    "current_page": 1,
    "total_pages": 2,
    "page_size": 10
  }
}
```

### Homework Endpoints

#### List Homework for a Lecture (Paginated)
```http
GET /api/courses/{course_id}/lectures/{lecture_id}/homeworks/?page=1&page_size=10
Authorization: Bearer your-access-token
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response:**
```json
{
  "count": 8,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "lecture": {
        "id": 1,
        "topic": "Introduction to Python Programming",
        "presentation": "python_intro_slides.pdf",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
      },
      "title": "Python Basics Assignment",
      "description": "Complete the following Python exercises...",
      "due_date": "2024-01-20T23:59:00Z",
      "created_by": {
        "id": 1,
        "email": "teacher@example.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "role": "teacher"
      },
      "created_at": "2024-01-15T14:00:00Z",
      "updated_at": "2024-01-15T14:00:00Z"
    }
  ],
  "page_info": {
    "current_page": 1,
    "total_pages": 1,
    "page_size": 10
  }
}
```

#### Create Homework Assignment
```http
POST /api/courses/{course_id}/lectures/{lecture_id}/homeworks/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "title": "Advanced Python Concepts",
  "description": "Implement the following advanced Python features...",
  "due_date": "2024-01-25T23:59:00Z"
}
```

#### Update Homework Assignment
```http
PUT /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "title": "Updated Python Assignment",
  "description": "Updated assignment description...",
  "due_date": "2024-01-30T23:59:00Z"
}
```

#### Delete Homework Assignment
```http
DELETE /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/
Authorization: Bearer your-access-token
```

### Homework Submission Endpoints

#### List Submissions for a Homework (Paginated)
```http
GET /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/?page=1&page_size=10
Authorization: Bearer your-access-token
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 100)

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "homework": {
        "id": 1,
        "title": "Python Basics Assignment",
        "description": "Complete the following Python exercises...",
        "due_date": "2024-01-20T23:59:00Z"
      },
      "student": {
        "id": 2,
        "email": "student@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "student"
      },
      "content": "Here is my solution to the Python assignment...",
      "submitted_at": "2024-01-18T15:30:00Z",
      "updated_at": "2024-01-18T15:30:00Z",
      "is_submitted": true
    }
  ],
  "page_info": {
    "current_page": 1,
    "total_pages": 1,
    "page_size": 10
  }
}
```

#### Create Homework Submission
```http
POST /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "content": "Here is my solution to the assignment..."
}
```

#### Update Homework Submission
```http
PATCH /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "content": "Updated solution content...",
  "is_submitted": true
}
```

#### Delete Homework Submission
```http
DELETE /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/
Authorization: Bearer your-access-token
```

#### Create Lecture (multipart upload)
Use multipart/form-data to upload the presentation file.
```http
POST /api/courses/{course_id}/lectures/
Authorization: Bearer your-access-token
Content-Type: multipart/form-data

topic=Introduction to Python Programming
presentation=@/path/to/python_intro_slides.pdf
```

#### Retrieve Lecture
```http
GET /api/courses/{course_id}/lectures/{lecture_id}/
Authorization: Bearer your-access-token
```

#### Update Lecture (Full)
```http
PUT /api/courses/{course_id}/lectures/{lecture_id}/
Authorization: Bearer your-access-token
Content-Type: multipart/form-data

topic=Advanced Python Concepts
presentation=@/path/to/advanced_python.pdf
```

#### Update Lecture (Partial)
```http
PATCH /api/courses/{course_id}/lectures/{lecture_id}/
Authorization: Bearer your-access-token
Content-Type: multipart/form-data (if replacing file) or application/json

{
  "topic": "Updated Topic Name"
}
```

### Grade Endpoints

#### List Grades for a Submission
```http
GET /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/
Authorization: Bearer your-access-token
```

#### Create Grade (Teacher)
```http
POST /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "grade": 92.5,
  "comments": "Great job!"
}
```

#### Update Grade (Teacher who graded)
```http
PATCH /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/{grade_id}/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "grade": 95.0,
  "comments": "Adjusted after review"
}
```

### Grade Comment Endpoints

#### List Comments on a Grade
```http
GET /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/{grade_id}/comments/
Authorization: Bearer your-access-token
```

#### Add Comment on a Grade (Teacher or submission owner)
```http
POST /api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/{grade_id}/comments/
Authorization: Bearer your-access-token
Content-Type: application/json

{
  "comment": "Please check question 3 again."
}
```

#### Delete Lecture
```http
DELETE /api/courses/{course_id}/lectures/{lecture_id}/
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
  "code": "ERR_FORBIDDEN",
  "message": "You don't have permission to perform this action",
  "detail": "Optional short detail",
  "details": "Optional long detail"
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
| Create Lecture | Yes | Yes* | No |
| View Lectures | Yes | Yes | Yes |
| Update Lecture | Yes | Yes* | No |
| Delete Lecture | Yes | Yes* | No |

*Only for courses where they are assigned as teachers

## Project Structure

```
online-course-management-system/
├── apps/
│   ├── courses/                    # Course management app
│   │   ├── models.py              # Course, CourseTeacher, CourseStudent, Lecture models
│   │   ├── views.py               # CourseViewSet, LectureViewSet (CRUD operations)
│   │   ├── serializers.py         # API serializers
│   │   ├── pagination.py          # Custom pagination classes
│   │   ├── permissions.py         # IsCoursePrimaryOwner permission
│   │   ├── admin.py               # Django admin configuration
│   │   ├── services/              # Service layer (business logic)
│   │   │   ├── protocols.py       # Service-level protocols (LectureService, OwnershipGuard)
│   │   │   ├── course.py          # CourseCreationService, CourseUpdateService
│   │   │   ├── user.py            # UserService
│   │   │   ├── relationship_manager.py # Course relationship management
│   │   │   ├── dtos/              # Data Transfer Objects
│   │   │   │   ├── course.py      # Course-related DTOs
│   │   │   │   ├── user.py        # User-related DTOs
│   │   │   │   └── lecture.py     # Lecture-related DTOs
│   │   │   ├── lecture/           # Lecture module
│   │   │   │   ├── services.py    # LectureCreationService, LectureUpdateService, LectureManagementService
│   │   │   │   ├── validation.py  # Lecture validation pipeline
│   │   │   │   └── __init__.py    # Lecture module exports
│   │   │   ├── shared/            # Shared components
│   │   │   │   ├── ownership_guard.py # CourseOwnershipGuard
│   │   │   │   └── __init__.py    # Shared module exports
│   │   │   └── validation/        # Validation layer
│   │   │       ├── base.py        # Base validator with shared logic
│   │   │       ├── creation.py    # Course creation validation
│   │   │       ├── update.py      # Course update validation
│   │   │       ├── user_role.py   # User role validation
│   │   │       ├── uniqueness.py  # Uniqueness validation
│   │   │       ├── business_rules.py # Business rule validation
│   │   │       └── interfaces.py  # Validation interfaces
│   │   └── migrations/            # Database migrations
│   ├── homeworks/                 # Homework management app
│   │   ├── models.py              # Homework, HomeworkSubmission models
│   │   ├── views.py               # HomeworkViewSet, HomeworkSubmissionViewSet (CRUD operations)
│   │   ├── serializers.py         # API serializers
│   │   ├── pagination.py          # Custom pagination classes
│   │   ├── admin.py               # Django admin configuration
│   │   ├── urls.py                # URL routing
│   │   ├── services/              # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── protocols.py       # Service interfaces
│   │   │   ├── homework/          # Homework-specific services
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py        # Homework DTOs
│   │   │   │   ├── validation.py  # Homework validation
│   │   │   │   └── services.py    # Homework business logic
│   │   │   ├── submission/        # Submission-specific services
│   │   │   │   ├── __init__.py
│   │   │   │   ├── dtos.py        # Submission DTOs
│   │   │   │   ├── validation.py  # Submission validation
│   │   │   │   └── services.py    # Submission business logic
│   │   │   └── shared/            # Shared services
│   │   │       ├── __init__.py
│   │   │       └── ownership_guard.py  # Homework ownership validation
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
6. **Protocol-based Interfaces**: Use ABC protocols for dependency inversion
7. **Enum-based Constants**: Eliminate magic strings throughout the codebase

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



## Testing

### Quick start

```bash
uv run pytest
```

- Uses `DJANGO_SETTINGS_MODULE=config.settings` from `pytest.ini`.
- Discovers tests matching `test_*.py` or `*_test.py`.
- Default options include `-q` (quiet) from `pytest.ini`.

### Run selected tests

- Single file:
```bash
uv run pytest apps/courses/test_courses_lectures.py
```

- Single test function:
```bash
uv run pytest apps/homeworks/test_homeworks.py::test_create_homework
```

- Filter by keyword:
```bash
uv run pytest -k "lecture and create"
```

### With coverage (optional)

Install coverage plugin:
```bash
uv add pytest-cov
```

Run with coverage report:
```bash
uv run pytest --cov=apps --cov-report=term-missing
```

### Notes

- Tests use the default SQLite database and run migrations automatically.
- If you use pip instead of uv, replace `uv run` with `python -m` (e.g., `python -m pytest`).
```mermaid 
erDiagram
    USER ||--o{ COURSE : "owns (primary_owner)"
    COURSE ||--o{ COURSETEACHER : "has teachers"
    COURSE ||--o{ COURSESTUDENT : "has students"
    USER ||--o{ COURSETEACHER : "teaches courses"
    USER ||--o{ COURSESTUDENT : "enrolled in courses"
    COURSE ||--o{ LECTURE : "has"
    LECTURE ||--o{ HOMEWORK : "has"
    HOMEWORK ||--o{ HOMEWORKSUBMISSION : "submitted for"
    USER ||--o{ HOMEWORK : "creates"
    USER ||--o{ HOMEWORKSUBMISSION : "submits"
    HOMEWORKSUBMISSION ||--|| HOMEWORKGRADE : "graded as"
    USER ||--o{ HOMEWORKGRADE : "grades"
    HOMEWORKGRADE ||--o{ GRADECOMMENT : "has comments"
    USER ||--o{ GRADECOMMENT : "writes"
    
    USER {
        int id
        string email
        string first_name
        string last_name
        string role
        datetime date_joined
        boolean is_active
    }
    
    COURSE {
        int id
        string name
        text description
        int primary_owner_id
        datetime created_at
        datetime updated_at
    }
    
    COURSETEACHER {
        int id
        int course_id
        int user_id
        datetime added_at
    }
    
    COURSESTUDENT {
        int id
        int course_id
        int user_id
        datetime enrolled_at
    }
    
    LECTURE {
        int id
        int course_id
        string topic
        file presentation
        datetime created_at
        datetime updated_at
    }
    
    HOMEWORK {
        int id
        int lecture_id
        string title
        text description
        datetime due_date
        int created_by_id
        datetime created_at
        datetime updated_at
    }
    
    HOMEWORKSUBMISSION {
        int id
        int homework_id
        int student_id
        text content
        datetime submitted_at
        datetime updated_at
        boolean is_submitted
    }
    
    HOMEWORKGRADE {
        int id
        int submission_id
        decimal grade
        text comments
        int graded_by_id
        datetime graded_at
        datetime updated_at
    }
    
    GRADECOMMENT {
        int id
        int grade_id
        int author_id
        text comment
        datetime created_at
        datetime updated_at
    }