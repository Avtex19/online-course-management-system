from dataclasses import dataclass, field
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.courses.models import Course, Lecture
from apps.courses.services.dtos import LectureCreationRequest, LectureUpdateRequest
from apps.courses.services.lecture.validation import LectureCreationValidator, LectureUpdateValidator
from apps.courses.services.shared.ownership_guard import CourseOwnershipGuard
from apps.courses.services.protocols import OwnershipGuard, LectureService
from common.enums import ModelFields


@dataclass
class LectureCreationService:
    validation_service: LectureCreationValidator = field(default_factory=LectureCreationValidator)
    ownership_guard: OwnershipGuard = field(default_factory=CourseOwnershipGuard)

    def create_lecture(self, request: LectureCreationRequest, course: Course, user) -> Lecture:
        """Create a new lecture with full validation"""
        self.ownership_guard.ensure_owner(course, user)
        
        validation_result = self.validation_service.validate_lecture_creation(request, course)
        
        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._create_lecture_with_validation(request, course)

    @transaction.atomic
    def _create_lecture_with_validation(self, request: LectureCreationRequest, course: Course) -> Lecture:
        """Create lecture in a transaction"""
        return Lecture.objects.create(
            course=course,
            topic=request.topic,
            presentation=request.presentation
        )


@dataclass
class LectureUpdateService:
    """Handles lecture updates with validation and business logic"""
    validation_service: LectureUpdateValidator = field(default_factory=LectureUpdateValidator)
    ownership_guard: OwnershipGuard = field(default_factory=CourseOwnershipGuard)

    def update_lecture(self, instance: Lecture, request: LectureUpdateRequest, user) -> Lecture:
        """Update an existing lecture with full validation"""
        # Validate ownership
        self.ownership_guard.ensure_owner(instance.course, user)
        
        # Validate request
        validation_result = self.validation_service.validate_lecture_update(request, instance)
        
        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._update_lecture_with_validation(instance, request)

    @transaction.atomic
    def _update_lecture_with_validation(self, instance: Lecture, request: LectureUpdateRequest) -> Lecture:
        """Update lecture in a transaction"""
        if request.topic is not None:
            instance.topic = request.topic
        if request.presentation is not None:
            instance.presentation = request.presentation
        
        instance.save()
        return instance


@dataclass
class LectureManagementService(LectureService):
    creation_service: LectureCreationService = field(default_factory=LectureCreationService)
    update_service: LectureUpdateService = field(default_factory=LectureUpdateService)
    ownership_guard: OwnershipGuard = field(default_factory=CourseOwnershipGuard)

    def create(self, *, course, user, validated_data) -> Lecture:
        """Create a new lecture"""
        request = LectureCreationRequest(
            topic=validated_data[ModelFields.TOPIC.value],
            presentation=validated_data[ModelFields.PRESENTATION.value],
            course_id=course.id
        )
        return self.creation_service.create_lecture(request, course, user)

    def update(self, *, instance, user, validated_data, partial=False) -> Lecture:
        """Update an existing lecture"""
        request = LectureUpdateRequest(
            lecture_id=instance.id,
            topic=validated_data.get(ModelFields.TOPIC.value),
            presentation=validated_data.get(ModelFields.PRESENTATION.value)
        )
        return self.update_service.update_lecture(instance, request, user)

    def delete(self, *, instance, user) -> None:
        """Delete a lecture"""
        self.ownership_guard.ensure_owner(instance.course, user)
        instance.delete()
