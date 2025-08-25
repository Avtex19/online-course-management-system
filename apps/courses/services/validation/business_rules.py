from typing import List, Optional
from rest_framework.exceptions import ValidationError
from common.enums import ErrorMessages
from .interfaces import BusinessRuleValidatorInterface


class BusinessRuleValidator(BusinessRuleValidatorInterface):

    def validate_primary_owner_not_in_teachers(self, primary_owner_id: int, teacher_ids: List[int]) -> None:
        """Validate that primary owner is not also listed as a teacher"""
        if primary_owner_id in teacher_ids:
            raise ValidationError(ErrorMessages.PRIMARY_OWNER_IS_ALREADY_TEACHER.value)
    
    def validate_course_name(self, name: str) -> None:
        """Validate that course name is not empty"""
        if not name or not name.strip():
            raise ValidationError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)
    
    def validate_primary_owner_id(self, primary_owner_id: int) -> None:
        """Validate that primary owner ID is positive"""
        if primary_owner_id <= 0:
            raise ValidationError(ErrorMessages.PRIMARY_OWNER_ID_POSITIVE.value)
    
    def validate_course_id(self, course_id: int) -> None:
        """Validate that course ID is positive"""
        if course_id <= 0:
            raise ValidationError(ErrorMessages.COURSE_ID_POSITIVE.value)
    
    def validate_course_name_for_update(self, name: Optional[str]) -> None:
        """Validate course name for updates (only if provided)"""
        if name is not None:
            self.validate_course_name(name)
    
    def validate_primary_owner_id_for_update(self, primary_owner_id: Optional[int]) -> None:
        """Validate primary owner ID for updates (only if provided)"""
        if primary_owner_id is not None:
            self.validate_primary_owner_id(primary_owner_id)
