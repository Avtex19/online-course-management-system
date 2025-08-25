from enum import Enum


class UserRole(Enum):
    TEACHER = "teacher"
    STUDENT = "student"

    @classmethod
    def choices(cls):
        return [(role.value, role.name.capitalize()) for role in cls]


class ErrorMessages(str, Enum):
    COURSE_DOESNT_EXIST = "Course does not exist"
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
    INVALID_TOKEN = "Invalid token: {error}"
    FIRST_NAME_REQUIRED = "First name cannot be empty"
    LAST_NAME_REQUIRED = "Last name cannot be empty"
    USER_IS_ALREADY_TEACHER = "User is already teacher"
    PRIMARY_OWNER_IS_ALREADY_TEACHER = "Primary owner is already teacher"
    COURSE_CANT_BE_EMPTY = "Course cannot be empty"
    PRIMARY_OWNER_ID_POSITIVE = "Primary owner id must be positive"
    COURSE_ID_POSITIVE = "Course id must be positive"
    COURSE_ALREADY_EXISTS_FOR_TEACHER = 'A course with this name already exists for this teacher'
    ONLY_PRIMARY_OWNER_ALLOWED = "Only the primary owner can perform this action"
    COURSE_ACCESS_DENIED = "You don't have permission to manage this course"
    LECTURE_TOPIC_ALREADY_EXISTS = "A lecture with topic '{topic}' already exists in this course"


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
    PASSWORD = "password"
    PASSWORD_CONFIRM = "password_confirm"
    ID = "id"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    LAST_LOGIN = "last_login"


class AuthHeaders(str, Enum):
    AUTH_HEADER = "Authorization"
    AUTH_HEADER_FALLBACK = "HTTP_AUTHORIZATION"
    BEARER_PREFIX = "Bearer "


class TokenFields(str, Enum):
    REFRESH = "refresh_token"
    ACCESS = "access_token"
    REFRESH_SHORT = "refresh"
    ACCESS_SHORT = "access"
    JTI = "jti"
    USER_ID = 'user_id'
    IAT = 'iat'
    EXP = 'exp'


class ValidationFields(str, Enum):
    NON_FIELD_ERRORS = "non_field_errors"
    DETAIL = "detail"


class ResponseKeys(str, Enum):
    MESSAGE = "message"
    USER = "user"
    TOKENS = "tokens"


class RelatedNames(str, Enum):
    OWNED_COURSES = "owned_courses"
    TEACHING_COURSES = "teaching_courses"
    ENROLLED_COURSES = "enrolled_courses"


class ModelVerboseNames(str, Enum):
    COURSE_TEACHER = "Course teacher"
    COURSE_TEACHERS = "Course teachers"
    COURSE_STUDENT = "Course student"
    COURSE_STUDENTS = "Course students"
    USER = "User"
    USERS = "Users"


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
    TEACHERS = "teachers"
    STUDENTS = "students"
    TOPIC = 'topic'
    PRESENTATION = 'presentation'
    COURSE_PK = "course_pk"


class SerializerFields(str, Enum):
    USER_ID = "user_id"
    TEACHER_IDS = "teacher_ids"
    STUDENT_IDS = "student_ids"
    PRIMARY_OWNER_ID = "primary_owner_id"
    TEACHER_COUNT = "teacher_count"
    STUDENT_COUNT = "student_count"


class FieldDisplayNames(str, Enum):
    PRIMARY_OWNER = "Primary owner"
    TEACHER = "Teacher"
    STUDENT = "Student"


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class RequestData(str, Enum):
    DATA = "data"


class ViewActions(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    LIST = "list"
    RETRIEVE = "retrieve"
    DESTROY = "destroy"
    PARTIAL = 'partial'


class URLPatterns(str, Enum):
    """URL patterns for routing"""
    COURSES = "courses"
    LECTURES = "lectures"
    COURSE_PK = "course_pk"
    PK = "pk"


class HTTPMethods(str, Enum):
    """HTTP methods for ViewSet actions"""
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"



