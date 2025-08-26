from dataclasses import dataclass, field
from typing import Optional
from rest_framework.exceptions import ValidationError

from apps.homeworks.models import Homework
from apps.courses.models import Lecture
from apps.homeworks.services.homework.dtos import HomeworkCreationRequest, HomeworkUpdateRequest, HomeworkValidationResult
from apps.homeworks.services.validation.interfaces import (
    HomeworkUniquenessValidatorInterface,
    HomeworkBusinessRuleValidatorInterface,
    HomeworkCreationValidatorInterface,
    HomeworkUpdateValidatorInterface
)
from apps.homeworks.services.validation.base import BaseValidator
from common.enums import ErrorMessages, ModelFields


@dataclass
class HomeworkUniquenessValidator(HomeworkUniquenessValidatorInterface):
    """Validates homework uniqueness within a lecture"""

    def validate_title_uniqueness(self, lecture: Lecture, title: str, exclude_homework_id: Optional[int] = None) -> None:
        """Validate that title is unique within the lecture"""
        queryset = Homework.objects.filter(lecture=lecture, title=title)
        if exclude_homework_id:
            queryset = queryset.exclude(id=exclude_homework_id)

        if queryset.exists():
            raise ValidationError(ErrorMessages.HOMEWORK_TITLE_ALREADY_EXISTS.value.format(title=title))


@dataclass
class HomeworkBusinessRuleValidator(HomeworkBusinessRuleValidatorInterface):
    """Validates homework business rules"""

    def validate_title(self, title: str) -> None:
        """Validate that title is not empty"""
        if not title or not title.strip():
            raise ValidationError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)

    def validate_title_for_update(self, title: Optional[str]) -> None:
        """Validate title for updates (only if provided)"""
        if title is not None:
            self.validate_title(title)

    def validate_homework_id(self, homework_id: int) -> None:
        """Validate that homework ID is positive"""
        if homework_id <= 0:
            raise ValidationError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass
class HomeworkCreationValidator(BaseValidator, HomeworkCreationValidatorInterface):
    """Validates homework creation requests"""
    uniqueness_validator: HomeworkUniquenessValidatorInterface = field(default_factory=HomeworkUniquenessValidator)
    business_rule_validator: HomeworkBusinessRuleValidatorInterface = field(default_factory=HomeworkBusinessRuleValidator)

    def validate_homework_creation(self, request: HomeworkCreationRequest, lecture: Lecture) -> HomeworkValidationResult:
        """Validate entire homework creation request"""
        context = HomeworkValidationContext(request=request, lecture=lecture)

        # Validation pipeline
        self._validate_basic_fields(context)
        self._validate_uniqueness(context)

        return HomeworkValidationResult(
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )

    def _validate_basic_fields(self, context: 'HomeworkValidationContext') -> None:
        try:
            self.business_rule_validator.validate_title(context.request.title)
        except ValidationError as e:
            context.errors.append(self._extract_clean_error_message(e))

    def _validate_uniqueness(self, context: 'HomeworkValidationContext') -> None:
        try:
            self.uniqueness_validator.validate_title_uniqueness(
                lecture=context.lecture,
                title=context.request.title
            )
        except ValidationError as e:
            context.errors.append(self._extract_clean_error_message(e))


@dataclass
class HomeworkUpdateValidator(BaseValidator, HomeworkUpdateValidatorInterface):
    """Validates homework update requests"""
    uniqueness_validator: HomeworkUniquenessValidatorInterface = field(default_factory=HomeworkUniquenessValidator)
    business_rule_validator: HomeworkBusinessRuleValidatorInterface = field(default_factory=HomeworkBusinessRuleValidator)

    def validate_homework_update(self, request: HomeworkUpdateRequest, instance: Homework) -> HomeworkValidationResult:
        """Validate homework update request"""
        context = HomeworkUpdateValidationContext(request=request, instance=instance)

        # Validation pipeline
        self._validate_basic_fields_for_update(context)
        self._validate_uniqueness_for_update(context)

        return HomeworkValidationResult(
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )

    def _validate_basic_fields_for_update(self, context: 'HomeworkUpdateValidationContext') -> None:
        """Validate basic fields for updates"""
        if context.request.title is not None:
            try:
                self.business_rule_validator.validate_title_for_update(context.request.title)
            except ValidationError as e:
                context.errors.append(self._extract_clean_error_message(e))

    def _validate_uniqueness_for_update(self, context: 'HomeworkUpdateValidationContext') -> None:
        """Validate uniqueness for updates"""
        if context.request.title is not None:
            try:
                self.uniqueness_validator.validate_title_uniqueness(
                    lecture=context.instance.lecture,
                    title=context.request.title,
                    exclude_homework_id=context.instance.id
                )
            except ValidationError as e:
                context.errors.append(self._extract_clean_error_message(e))


@dataclass
class HomeworkValidationContext:
    """Context for homework creation validation"""
    request: HomeworkCreationRequest
    lecture: Lecture
    errors: list[str] = field(default_factory=list)


@dataclass
class HomeworkUpdateValidationContext:
    """Context for homework update validation"""
    request: HomeworkUpdateRequest
    instance: Homework
    errors: list[str] = field(default_factory=list)
