from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

from common.enums import UserRole

if TYPE_CHECKING:
    from apps.courses.services.dtos import UserValidationResult, CourseValidationResult, CourseUpdateValidationResult
else:
    from apps.courses.services.dtos import UserValidationResult


class UserRoleValidatorInterface(ABC):
    """Interface for user role validation"""
    
    @abstractmethod
    def validate_user_role(self, user_id: int, role: UserRole) -> UserValidationResult:
        """Validate that user exists and has the required role"""
        pass


class CourseUniquenessValidatorInterface(ABC):
    """Interface for course uniqueness validation"""
    
    @abstractmethod
    def validate_course_uniqueness(self, name: str, primary_owner_id: int) -> None:
        """Validate that course name is unique for the given teacher"""
        pass
    
    @abstractmethod
    def validate_course_uniqueness_for_update(self, course_id: int, name: str, primary_owner_id: int) -> None:
        """Validate that course name is unique for the given teacher during update"""
        pass


class BusinessRuleValidatorInterface(ABC):
    """Interface for course business rule validation"""
    
    @abstractmethod
    def validate_primary_owner_not_in_teachers(self, primary_owner_id: int, teacher_ids: List[int]) -> None:
        """Validate that primary owner is not also listed as a teacher"""
        pass
    
    @abstractmethod
    def validate_course_name(self, name: str) -> None:
        """Validate that course name is not empty"""
        pass
    
    @abstractmethod
    def validate_primary_owner_id(self, primary_owner_id: int) -> None:
        """Validate that primary owner ID is positive"""
        pass
    
    @abstractmethod
    def validate_course_id(self, course_id: int) -> None:
        """Validate that course ID is positive"""
        pass
    
    @abstractmethod
    def validate_course_name_for_update(self, name: Optional[str]) -> None:
        """Validate course name for updates (only if provided)"""
        pass
    
    @abstractmethod
    def validate_primary_owner_id_for_update(self, primary_owner_id: Optional[int]) -> None:
        """Validate primary owner ID for updates (only if provided)"""
        pass


class CourseCreationValidatorInterface(ABC):

    @abstractmethod
    def validate_course_creation(self, request) -> 'CourseValidationResult':
        """Validate entire course creation request and return structured result"""
        pass


class CourseUpdateValidatorInterface(ABC):
    """Interface for course update validation orchestration"""
    
    @abstractmethod
    def validate_course_update(self, request) -> 'CourseUpdateValidationResult':
        """Validate course update request and return structured result"""
        pass
