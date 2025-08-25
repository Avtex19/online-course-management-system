from dataclasses import dataclass, field
from typing import Optional
from rest_framework.exceptions import ValidationError

from apps.courses.models import Course, Lecture
from apps.courses.services.dtos import LectureCreationRequest, LectureUpdateRequest, LectureValidationResult
from apps.courses.services.validation.base import BaseValidator
from common.enums import ErrorMessages


@dataclass
class LectureUniquenessValidator:
    """Validates lecture uniqueness within a course"""

    def validate_topic_uniqueness(self, course: Course, topic: str, exclude_lecture_id: Optional[int] = None) -> None:
        """Validate that topic is unique within the course"""
        queryset = Lecture.objects.filter(course=course, topic=topic)
        if exclude_lecture_id:
            queryset = queryset.exclude(id=exclude_lecture_id)
        
        if queryset.exists():
            raise ValidationError(ErrorMessages.LECTURE_TOPIC_ALREADY_EXISTS.value.format(topic=topic))


@dataclass
class LectureBusinessRuleValidator:

    def validate_topic(self, topic: str) -> None:
        """Validate that topic is not empty"""
        if not topic or not topic.strip():
            raise ValidationError(ErrorMessages.COURSE_CANT_BE_EMPTY.value)

    def validate_topic_for_update(self, topic: Optional[str]) -> None:
        """Validate topic for updates (only if provided)"""
        if topic is not None:
            self.validate_topic(topic)

    def validate_lecture_id(self, lecture_id: int) -> None:
        """Validate that lecture ID is positive"""
        if lecture_id <= 0:
            raise ValidationError(ErrorMessages.COURSE_ID_POSITIVE.value)


@dataclass
class LectureCreationValidator(BaseValidator):
    uniqueness_validator: LectureUniquenessValidator = field(default_factory=LectureUniquenessValidator)
    business_rule_validator: LectureBusinessRuleValidator = field(default_factory=LectureBusinessRuleValidator)

    def validate_lecture_creation(self, request: LectureCreationRequest, course: Course) -> LectureValidationResult:
        """Validate entire lecture creation request"""
        context = LectureValidationContext(request=request, course=course)
        
        # Validation pipeline
        self._validate_basic_fields(context)
        self._validate_uniqueness(context)
        
        return LectureValidationResult(
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )

    def _validate_basic_fields(self, context: 'LectureValidationContext') -> None:
        """Validate basic lecture fields"""
        try:
            self.business_rule_validator.validate_topic(context.request.topic)
        except ValidationError as e:
            context.errors.append(self._extract_clean_error_message(e))

    def _validate_uniqueness(self, context: 'LectureValidationContext') -> None:
        """Validate lecture uniqueness"""
        try:
            self.uniqueness_validator.validate_topic_uniqueness(
                course=context.course,
                topic=context.request.topic
            )
        except ValidationError as e:
            context.errors.append(self._extract_clean_error_message(e))


@dataclass
class LectureUpdateValidator(BaseValidator):
    """Validates lecture update requests"""
    uniqueness_validator: LectureUniquenessValidator = field(default_factory=LectureUniquenessValidator)
    business_rule_validator: LectureBusinessRuleValidator = field(default_factory=LectureBusinessRuleValidator)

    def validate_lecture_update(self, request: LectureUpdateRequest, instance: Lecture) -> LectureValidationResult:
        """Validate lecture update request"""
        context = LectureUpdateValidationContext(request=request, instance=instance)
        
        self._validate_basic_fields_for_update(context)
        self._validate_uniqueness_for_update(context)
        
        return LectureValidationResult(
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )

    def _validate_basic_fields_for_update(self, context: 'LectureUpdateValidationContext') -> None:
        """Validate basic fields for updates"""
        if context.request.topic is not None:
            try:
                self.business_rule_validator.validate_topic_for_update(context.request.topic)
            except ValidationError as e:
                context.errors.append(self._extract_clean_error_message(e))

    def _validate_uniqueness_for_update(self, context: 'LectureUpdateValidationContext') -> None:
        """Validate uniqueness for updates"""
        if context.request.topic is not None:
            try:
                self.uniqueness_validator.validate_topic_uniqueness(
                    course=context.instance.course,
                    topic=context.request.topic,
                    exclude_lecture_id=context.instance.id
                )
            except ValidationError as e:
                context.errors.append(self._extract_clean_error_message(e))


# Validation contexts
@dataclass
class LectureValidationContext:
    """Context for lecture creation validation"""
    request: LectureCreationRequest
    course: Course
    errors: list[str] = field(default_factory=list)


@dataclass
class LectureUpdateValidationContext:
    """Context for lecture update validation"""
    request: LectureUpdateRequest
    instance: Lecture
    errors: list[str] = field(default_factory=list)
