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


class UserFields(str, Enum):
    EMAIL = "email"
    IS_STAFF = "is_staff"
    IS_SUPERUSER = "is_superuser"
    IS_ACTIVE = "is_active"





