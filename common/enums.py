from enum import Enum


class UserRole(Enum):
    TEACHER = "teacher"
    STUDENT = "student"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.capitalize()) for role in cls]


class ErrorMessages(str, Enum):
    PASSWORDS_DO_NOT_MATCH = "Passwords do not match"
    EMAIL_REQUIRED = "The Email field must be set"
    SUPERUSER_STAFF_REQUIRED = "Superuser must have is_staff=True."
    SUPERUSER_PERMISSION_REQUIRED = "Superuser must have is_superuser=True."
    INVALID_CREDENTIALS = "Invalid email or password"
    INACTIVE_ACCOUNT = "Account is disabled"
    REFRESH_TOKEN_REQUIRED = "Refresh token is required"
    ACCESS_TOKEN_REQUIRED = "Access token is required"
    TOKEN_BLACKLISTED = "Token is blacklisted"
    TOKEN_NOT_TRACKED = "Token not tracked"
    TOKEN_MISSING_JTI = "Token missing jti claim"
    USER_MUST_BE_TEACHER = "User must be teacher"
    USER_MUST_BE_STUDENT = "User must be student"
    USER_DOESNT_EXIST = "User does not exist"


class SuccessMessages(str, Enum):
    LOGOUT_SUCCESS = "Successfully logged out"
    REGISTRATION_SUCCESS = "Account created successfully"
    LOGIN_SUCCESS = "Login successful"


class UserFields(str, Enum):
    EMAIL = "email"
    IS_STAFF = "is_staff"
    IS_SUPERUSER = "is_superuser"
    IS_ACTIVE = "is_active"
    ROLE = "role"


class AuthHeaders(str, Enum):
    AUTH_HEADER = "Authorization"
    AUTH_HEADER_FALLBACK = "HTTP_AUTHORIZATION"
    BEARER_PREFIX = "Bearer "


class TokenFields(str, Enum):
    REFRESH = "refresh_token"
    ACCESS = "access_token"
    JTI = "jti"


class ResponseKeys(str, Enum):
    MESSAGE = "message"


class RelatedNames(str, Enum):
    OWNED_COURSES = "owned_courses"
    TEACHING_COURSES = "teaching_courses"
    ENROLLED_COURSES = "enrolled_courses"


class ModelVerboseNames(str, Enum):
    COURSE_TEACHER = "Course teacher"
    COURSE_TEACHERS = "Course teachers"
    COURSE_STUDENT = "Course student"
    COURSE_STUDENTS = "Course students"


class ModelFields(str, Enum):
    COURSE = "course"
    USER = "user"
    NAME = "name"
    DESCRIPTION = "description"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    ID = 'id'
    PRIMARY_OWNER = "primary_owner"
    ENROLLED_AT = "enrolled_at"
    ADDED_AT = "added_at"


class SerializerFields(str, Enum):
    USER_ID = "user_id"
    TEACHER_IDS = "teacher_ids"
    STUDENT_IDS = "student_ids"
    PRIMARY_OWNER_ID = "primary_owner_id"
    TEACHER_COUNT = "teacher_count"
    STUDENT_COUNT = "student_count"

