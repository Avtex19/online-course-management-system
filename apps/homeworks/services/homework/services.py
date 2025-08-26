from dataclasses import dataclass, field
from django.db import transaction
from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.homeworks.models import Homework
from apps.courses.models import Lecture
from apps.homeworks.services.homework.dtos import HomeworkCreationRequest, HomeworkUpdateRequest
from apps.homeworks.services.homework.validation import HomeworkCreationValidator, HomeworkUpdateValidator
from apps.homeworks.services.validation.interfaces import HomeworkCreationValidatorInterface, HomeworkUpdateValidatorInterface
from apps.homeworks.services.shared.ownership_guard import HomeworkOwnershipGuardImpl
from apps.homeworks.services.protocols import HomeworkOwnershipGuard, HomeworkService
from common.enums import ModelFields, ErrorMessages, UserRole


@dataclass
class HomeworkCreationService:
    """Handles homework creation with validation and business logic"""
    validation_service: HomeworkCreationValidatorInterface = field(default_factory=HomeworkCreationValidator)
    ownership_guard: HomeworkOwnershipGuard = field(default_factory=HomeworkOwnershipGuardImpl)

    def create_homework(self, request: HomeworkCreationRequest, lecture: Lecture, user) -> Homework:
        """Create a new homework with full validation"""
        # Validate role (only teachers can create homework)
        if user.role != UserRole.TEACHER.value:
            raise PermissionDenied(ErrorMessages.USER_MUST_BE_TEACHER.value)
        
        # Validate ownership (user must be course owner or assigned teacher)
        course = lecture.course
        
        # Check if user is course owner or assigned teacher
        if course.primary_owner_id != user.id and not course.teachers.filter(id=user.id).exists():
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        # Validate request
        validation_result = self.validation_service.validate_homework_creation(request, lecture)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._create_homework_with_validation(request, lecture, user)

    @transaction.atomic
    def _create_homework_with_validation(self, request: HomeworkCreationRequest, lecture: Lecture, user) -> Homework:
        """Create homework in a transaction"""
        return Homework.objects.create(
            lecture=lecture,
            title=request.title,
            description=request.description,
            due_date=request.due_date,
            created_by=user
        )


@dataclass
class HomeworkUpdateService:
    """Handles homework updates with validation and business logic"""
    validation_service: HomeworkUpdateValidatorInterface = field(default_factory=HomeworkUpdateValidator)
    ownership_guard: HomeworkOwnershipGuard = field(default_factory=HomeworkOwnershipGuardImpl)

    def update_homework(self, instance: Homework, request: HomeworkUpdateRequest, user) -> Homework:
        """Update an existing homework with full validation"""
        self.ownership_guard.ensure_owner(instance, user)

        validation_result = self.validation_service.validate_homework_update(request, instance)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._update_homework_with_validation(instance, request)

    @transaction.atomic
    def _update_homework_with_validation(self, instance: Homework, request: HomeworkUpdateRequest) -> Homework:
        """Update homework in a transaction"""
        if request.title is not None:
            instance.title = request.title
        if request.description is not None:
            instance.description = request.description
        if request.due_date is not None:
            instance.due_date = request.due_date

        instance.save()
        return instance


@dataclass
class HomeworkManagementService(HomeworkService):
    """Composite service that handles all homework operations"""
    creation_service: HomeworkCreationService = field(default_factory=HomeworkCreationService)
    update_service: HomeworkUpdateService = field(default_factory=HomeworkUpdateService)
    ownership_guard: HomeworkOwnershipGuard = field(default_factory=HomeworkOwnershipGuardImpl)

    def create(self, *, lecture, user, validated_data) -> Homework:
        """Create a new homework"""
        request = HomeworkCreationRequest(
            title=validated_data[ModelFields.TITLE.value],
            description=validated_data[ModelFields.DESCRIPTION.value],
            due_date=validated_data[ModelFields.DUE_DATE.value],
            lecture_id=lecture.id
        )
        return self.creation_service.create_homework(request, lecture, user)

    def update(self, *, instance, user, validated_data, partial=False) -> Homework:
        """Update an existing homework"""
        request = HomeworkUpdateRequest(
            homework_id=instance.id,
            title=validated_data.get(ModelFields.TITLE.value),
            description=validated_data.get(ModelFields.DESCRIPTION.value),
            due_date=validated_data.get(ModelFields.DUE_DATE.value)
        )
        return self.update_service.update_homework(instance, request, user)

    def delete(self, *, instance, user) -> None:
        """Delete a homework"""
        self.ownership_guard.ensure_owner(instance, user)
        instance.delete()

    def get_homeworks_for_lecture(self, *, lecture_id):
        """Get homeworks for a specific lecture"""
        from apps.homeworks.models import Homework
        
        return (
            Homework.objects
            .select_related(ModelFields.LECTURE.value, ModelFields.CREATED_BY.value)
            .filter(lecture_id=lecture_id)
        )
