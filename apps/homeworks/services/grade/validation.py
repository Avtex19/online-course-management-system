from dataclasses import dataclass, field
from typing import List, Optional
from rest_framework.exceptions import ValidationError

from apps.homeworks.models import HomeworkSubmission, HomeworkGrade
from apps.homeworks.services.grade.dtos import GradeCreationRequest, GradeUpdateRequest, GradeValidationResult
from apps.homeworks.services.validation.interfaces import (
    GradeUniquenessValidatorInterface, GradeBusinessRuleValidatorInterface,
    GradeCreationValidatorInterface, GradeUpdateValidatorInterface
)
from apps.homeworks.services.validation.base import BaseValidator
from common.enums import ErrorMessages, UserRole


@dataclass
class GradeUniquenessValidator(GradeUniquenessValidatorInterface):
    """Validates grade uniqueness"""

    def validate_grade_uniqueness(self, submission: HomeworkSubmission, exclude_grade_id: Optional[int] = None) -> None:
        """Validate that submission has only one grade"""
        queryset = HomeworkGrade.objects.filter(submission=submission)
        if exclude_grade_id:
            queryset = queryset.exclude(id=exclude_grade_id)
            
        if queryset.exists():
            raise ValidationError(ErrorMessages.GRADE_ALREADY_EXISTS.value)


@dataclass
class GradeBusinessRuleValidator(GradeBusinessRuleValidatorInterface):
    """Validates grade business rules"""

    def validate_grade_value(self, grade: Optional[float]) -> None:
        """Validate that grade is within valid range (0-100)"""
        if grade is not None and (grade < 0 or grade > 100):
            raise ValidationError(ErrorMessages.GRADE_OUT_OF_RANGE.value)

    def validate_grade_value_for_update(self, grade: Optional[float]) -> None:
        """Validate grade value for updates (only if provided)"""
        if grade is not None:
            self.validate_grade_value(grade)

    def validate_grade_id(self, grade_id: int) -> None:
        """Validate that grade ID is positive"""
        if grade_id <= 0:
            raise ValidationError(ErrorMessages.GRADE_DOESNT_EXIST.value)


@dataclass
class GradeCreationValidator(GradeCreationValidatorInterface, BaseValidator):
    uniqueness_validator: GradeUniquenessValidatorInterface = field(default_factory=GradeUniquenessValidator)
    business_rule_validator: GradeBusinessRuleValidatorInterface = field(default_factory=GradeBusinessRuleValidator)

    def validate_grade_creation(self, request: GradeCreationRequest, user_id: int) -> GradeValidationResult:
        """Validate entire grade creation request using pipeline pattern"""
        errors = []
        
        try:
            self._validate_basic_fields(request)
            self._validate_submission_exists(request.submission_id)
            self._validate_grade_uniqueness(request.submission_id)
            self._validate_user_is_teacher(user_id)
        except ValidationError as e:
            errors.append(self._extract_clean_error_message(e))
        
        return GradeValidationResult(is_valid=len(errors) == 0, errors=errors)

    def _validate_basic_fields(self, request: GradeCreationRequest) -> None:
        """Validate basic fields"""
        self.business_rule_validator.validate_grade_value(request.grade)

    def _validate_submission_exists(self, submission_id: int) -> None:
        """Validate that submission exists"""
        try:
            HomeworkSubmission.objects.get(id=submission_id)
        except HomeworkSubmission.DoesNotExist:
            raise ValidationError(ErrorMessages.SUBMISSION_DOESNT_EXIST.value)

    def _validate_grade_uniqueness(self, submission_id: int) -> None:
        """Validate grade uniqueness"""
        submission = HomeworkSubmission.objects.get(id=submission_id)
        self.uniqueness_validator.validate_grade_uniqueness(submission)

    def _validate_user_is_teacher(self, user_id: int) -> None:
        """Validate that user is a teacher"""
        user = self.user_role_validator.validate_user_role(user_id, UserRole.TEACHER)


@dataclass
class GradeUpdateValidator(GradeUpdateValidatorInterface, BaseValidator):
    business_rule_validator: GradeBusinessRuleValidatorInterface = field(default_factory=GradeBusinessRuleValidator)

    def validate_grade_update(self, request: GradeUpdateRequest, instance: HomeworkGrade) -> GradeValidationResult:
        """Validate entire grade update request using pipeline pattern"""
        errors = []
        
        try:
            self._validate_basic_fields(request)
            self._validate_grade_exists(request.grade_id)
            self._validate_user_is_teacher(instance.graded_by_id)
        except ValidationError as e:
            errors.append(self._extract_clean_error_message(e))
        
        return GradeValidationResult(is_valid=len(errors) == 0, errors=errors)

    def _validate_basic_fields(self, request: GradeUpdateRequest) -> None:
        """Validate basic fields"""
        self.business_rule_validator.validate_grade_value_for_update(request.grade)

    def _validate_grade_exists(self, grade_id: int) -> None:
        """Validate that grade exists"""
        self.business_rule_validator.validate_grade_id(grade_id)

    def _validate_user_is_teacher(self, graded_by_id: int) -> None:
        """Validate that user is a teacher"""
        user = self.user_role_validator.validate_user_role(graded_by_id, UserRole.TEACHER)
