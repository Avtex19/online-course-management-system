from .interfaces import (
    UserRoleValidatorInterface,
    CourseUniquenessValidatorInterface, 
    BusinessRuleValidatorInterface,
    CourseCreationValidatorInterface,
    CourseUpdateValidatorInterface
)
from .user_role import UserRoleValidator
from .uniqueness import CourseUniquenessValidator
from .business_rules import BusinessRuleValidator
from .creation import CourseCreationValidator
from .update import CourseUpdateValidator

# Backward compatibility - provide the old interface
# This acts as a facade that implements the old monolithic interface
class CourseValidationService:
    """Facade that maintains backward compatibility while using the new segregated validators"""
    
    def __init__(self):
        self.creation_validator = CourseCreationValidator()
        self.update_validator = CourseUpdateValidator()
    
    def validate_course_creation(self, request):
        """Delegate to the creation validator"""
        return self.creation_validator.validate_course_creation(request)
    
    def validate_course_update(self, request):
        """Delegate to the update validator"""
        return self.update_validator.validate_course_update(request)

__all__ = [
    # Interfaces
    'UserRoleValidatorInterface',
    'CourseUniquenessValidatorInterface',
    'BusinessRuleValidatorInterface', 
    'CourseCreationValidatorInterface',
    'CourseUpdateValidatorInterface',
    
    # Concrete implementations
    'UserRoleValidator',
    'CourseUniquenessValidator',
    'BusinessRuleValidator',
    'CourseCreationValidator',
    'CourseUpdateValidator',
    
    # Backward compatibility
    'CourseValidationService',
]
