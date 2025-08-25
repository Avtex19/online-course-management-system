from .user import UserService
from .course import CourseCreationService, CourseUpdateService
from .shared import CourseOwnershipGuard
from .lecture import LectureManagementService
from .relationship_manager import (
    CourseRelationshipManager, 
    CourseRelationshipManagerInterface,
    CourseTeacherManagerInterface,
    CourseStudentManagerInterface,
    CourseRelationshipUpdaterInterface
)
from .validation import (
    CourseValidationService,
    UserRoleValidatorInterface,
    CourseUniquenessValidatorInterface,
    BusinessRuleValidatorInterface,
    CourseCreationValidatorInterface,
    CourseUpdateValidatorInterface,
    UserRoleValidator,
    CourseUniquenessValidator,
    BusinessRuleValidator,
    CourseCreationValidator,
    CourseUpdateValidator
)
from .dtos import CourseCreationRequest, CourseUpdateRequest, CourseValidationResult, CourseUpdateValidationResult, UserValidationResult, LectureCreationRequest, LectureUpdateRequest, LectureValidationResult

__all__ = [
    'UserService',
    'CourseCreationService',
    'CourseUpdateService',
    
    # Shared services
    'CourseOwnershipGuard',
    
    # Lecture services
    'LectureManagementService',
    
    # Relationship management
    'CourseRelationshipManager',
    'CourseRelationshipManagerInterface',
    'CourseTeacherManagerInterface',
    'CourseStudentManagerInterface', 
    'CourseRelationshipUpdaterInterface',
    
    # Backward compatible facade
    'CourseValidationService',
    
    # ISP-compliant interfaces
    'UserRoleValidatorInterface',
    'CourseUniquenessValidatorInterface',
    'BusinessRuleValidatorInterface',
    'CourseCreationValidatorInterface',
    'CourseUpdateValidatorInterface',
    
    # ISP-compliant implementations
    'UserRoleValidator',
    'CourseUniquenessValidator',
    'BusinessRuleValidator',
    'CourseCreationValidator',
    'CourseUpdateValidator',
    
    # DTOs
    'CourseCreationRequest',
    'CourseUpdateRequest',
    'CourseValidationResult',
    'CourseUpdateValidationResult',
    'UserValidationResult',
    'LectureCreationRequest',
    'LectureUpdateRequest',
    'LectureValidationResult',
]
