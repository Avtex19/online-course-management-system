from dataclasses import dataclass, field
from typing import Optional
from rest_framework.exceptions import ValidationError

from apps.homeworks.models import HomeworkSubmission, Homework
from apps.homeworks.services.submission.dtos import SubmissionCreationRequest, SubmissionUpdateRequest, SubmissionValidationResult
from apps.homeworks.services.validation.interfaces import (
    SubmissionUniquenessValidatorInterface,
    SubmissionBusinessRuleValidatorInterface,
    SubmissionCreationValidatorInterface,
    SubmissionUpdateValidatorInterface
)
from apps.homeworks.services.validation.base import BaseValidator
from common.enums import ErrorMessages, ModelFields
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dtos import SubmissionValidationContext, SubmissionUpdateValidationContext


@dataclass
class SubmissionUniquenessValidator(SubmissionUniquenessValidatorInterface):
    """Validates submission uniqueness for a homework"""

    def validate_submission_uniqueness(self, homework: Homework, student_id: int, exclude_submission_id: Optional[int] = None) -> None:
        """Validate that student has only one submission per homework"""
        queryset = HomeworkSubmission.objects.filter(homework=homework, student_id=student_id)
        if exclude_submission_id:
            queryset = queryset.exclude(id=exclude_submission_id)

        if queryset.exists():
            raise ValidationError(ErrorMessages.SUBMISSION_ALREADY_EXISTS.value)


@dataclass
class SubmissionBusinessRuleValidator(SubmissionBusinessRuleValidatorInterface):
    """Validates submission business rules"""

    def validate_content(self, content: str) -> None:
        """Validate that content is not empty"""
        if not content or not content.strip():
            raise ValidationError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)

    def validate_content_for_update(self, content: Optional[str]) -> None:
        """Validate content for updates (only if provided)"""
        if content is not None:
            self.validate_content(content)

    def validate_submission_id(self, submission_id: int) -> None:
        """Validate that submission ID is positive"""
        if submission_id <= 0:
            raise ValidationError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass
class SubmissionCreationValidator(BaseValidator, SubmissionCreationValidatorInterface):
    """Validates submission creation requests"""
    uniqueness_validator: SubmissionUniquenessValidatorInterface = field(default_factory=SubmissionUniquenessValidator)
    business_rule_validator: SubmissionBusinessRuleValidatorInterface = field(default_factory=SubmissionBusinessRuleValidator)

    def validate_submission_creation(self, request: SubmissionCreationRequest, homework: Homework, student_id: int) -> SubmissionValidationResult:
        """Validate entire submission creation request"""
        context = SubmissionValidationContext(request=request, homework=homework, student_id=student_id)

        # Validation pipeline
        self._validate_basic_fields(context)
        self._validate_uniqueness(context)

        return SubmissionValidationResult(
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )

    def _validate_basic_fields(self, context: 'SubmissionValidationContext') -> None:
        """Validate basic submission fields"""
        try:
            self.business_rule_validator.validate_content(context.request.content)
        except ValidationError as e:
            context.errors.append(self._extract_clean_error_message(e))

    def _validate_uniqueness(self, context: 'SubmissionValidationContext') -> None:
        """Validate submission uniqueness"""
        try:
            self.uniqueness_validator.validate_submission_uniqueness(
                homework=context.homework,
                student_id=context.student_id
            )
        except ValidationError as e:
            context.errors.append(self._extract_clean_error_message(e))


@dataclass
class SubmissionUpdateValidator(BaseValidator, SubmissionUpdateValidatorInterface):
    """Validates submission update requests"""
    uniqueness_validator: SubmissionUniquenessValidatorInterface = field(default_factory=SubmissionUniquenessValidator)
    business_rule_validator: SubmissionBusinessRuleValidatorInterface = field(default_factory=SubmissionBusinessRuleValidator)

    def validate_submission_update(self, request: SubmissionUpdateRequest, instance: HomeworkSubmission) -> SubmissionValidationResult:
        """Validate submission update request"""
        context = SubmissionUpdateValidationContext(request=request, instance=instance)

        # Validation pipeline
        self._validate_basic_fields_for_update(context)

        return SubmissionValidationResult(
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )

    def _validate_basic_fields_for_update(self, context: 'SubmissionUpdateValidationContext') -> None:
        """Validate basic fields for updates"""
        if context.request.content is not None:
            try:
                self.business_rule_validator.validate_content_for_update(context.request.content)
            except ValidationError as e:
                context.errors.append(self._extract_clean_error_message(e))


# Validation contexts
@dataclass
class SubmissionValidationContext:
    """Context for submission creation validation"""
    request: SubmissionCreationRequest
    homework: Homework
    student_id: int
    errors: list[str] = field(default_factory=list)


@dataclass
class SubmissionUpdateValidationContext:
    """Context for submission update validation"""
    request: SubmissionUpdateRequest
    instance: HomeworkSubmission
    errors: list[str] = field(default_factory=list)
