from .interfaces import (
    UserRoleValidatorInterface,
    CourseUniquenessValidatorInterface,
    BusinessRuleValidatorInterface,
    CourseCreationValidatorInterface,
    CourseUpdateValidatorInterface
)
from .base import BaseValidator
from .user_role import UserRoleValidator
from .uniqueness import CourseUniquenessValidator
from .business_rules import BusinessRuleValidator
from .creation import CourseCreationValidator
from .update import CourseUpdateValidator


class CourseValidationService:

    def __init__(self):
        self.creation_validator = CourseCreationValidator()
        self.update_validator = CourseUpdateValidator()

    def validate_course_creation(self, request):
        return self.creation_validator.validate_course_creation(request)

    def validate_course_update(self, request):
        return self.update_validator.validate_course_update(request)


__all__ = [
    'UserRoleValidatorInterface',
    'CourseUniquenessValidatorInterface',
    'BusinessRuleValidatorInterface',
    'CourseCreationValidatorInterface',
    'CourseUpdateValidatorInterface',

    'BaseValidator',

    'UserRoleValidator',
    'CourseUniquenessValidator',
    'BusinessRuleValidator',
    'CourseCreationValidator',
    'CourseUpdateValidator',

    'CourseValidationService',
]
