from dataclasses import dataclass, field
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.courses.models import Course
from .dtos import CourseCreationRequest, CourseUpdateRequest, CourseValidationResult, CourseUpdateValidationResult
from .validation import (
    CourseCreationValidator,
    CourseUpdateValidator,
    CourseCreationValidatorInterface,
    CourseUpdateValidatorInterface
)
from .relationship_manager import CourseRelationshipManager, CourseRelationshipManagerInterface


@dataclass
class CourseCreationService:
    validation_service: CourseCreationValidatorInterface = field(default_factory=CourseCreationValidator)
    relationship_manager: CourseRelationshipManagerInterface = field(default_factory=CourseRelationshipManager)

    def create_course(self, request: CourseCreationRequest) -> Course:
        validation_result = self.validation_service.validate_course_creation(request)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._create_course_with_relationships(request, validation_result)

    @transaction.atomic
    def _create_course_with_relationships(
            self,
            request: CourseCreationRequest,
            validation_result: CourseValidationResult
    ) -> Course:
        """Create course and establish all relationships in a transaction
        Atomic transaction ensures if any part fails  the database rolls back for avoiding half created things"""
        course = Course.objects.create(
            name=request.name,
            description=request.description,
            primary_owner=validation_result.primary_owner.user
        )

        # Establish relationships using dedicated manager
        self.relationship_manager.set_teachers(course, validation_result.teachers)
        self.relationship_manager.set_students(course, validation_result.students)

        return course


@dataclass
class CourseUpdateService:
    """Handles course update logic using dependency injection"""
    validation_service: CourseUpdateValidatorInterface = field(default_factory=CourseUpdateValidator)
    relationship_manager: CourseRelationshipManagerInterface = field(default_factory=CourseRelationshipManager)

    def update_course(self, instance: Course, request: CourseUpdateRequest) -> Course:
        """Update an existing course with all validations and relationships"""
        # Validate all inputs
        validation_result = self.validation_service.validate_course_update(request)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._update_course_with_relationships(instance, request, validation_result)

    @transaction.atomic
    def _update_course_with_relationships(
            self,
            instance: Course,
            request: CourseUpdateRequest,
            validation_result: CourseUpdateValidationResult
    ) -> Course:
        if request.name is not None:
            instance.name = request.name
        if request.description is not None:
            instance.description = request.description

        if validation_result.primary_owner is not None:
            instance.primary_owner = validation_result.primary_owner.user

        instance.save()

        self.relationship_manager.update_teachers(instance, validation_result.teachers)
        self.relationship_manager.update_students(instance, validation_result.students)

        return instance
