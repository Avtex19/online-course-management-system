from dataclasses import dataclass, field
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.homeworks.models import HomeworkSubmission, Homework
from apps.homeworks.services.submission.dtos import SubmissionCreationRequest, SubmissionUpdateRequest, SubmissionValidationResult
from apps.homeworks.services.submission.validation import SubmissionCreationValidator, SubmissionUpdateValidator
from apps.homeworks.services.validation.interfaces import SubmissionCreationValidatorInterface, SubmissionUpdateValidatorInterface
from apps.homeworks.services.shared.ownership_guard import SubmissionOwnershipGuardImpl
from apps.homeworks.services.protocols import SubmissionOwnershipGuard, SubmissionService
from common.enums import ModelFields, UserRole, ErrorMessages


@dataclass
class SubmissionCreationService:
    """Handles submission creation with validation and business logic"""
    validation_service: SubmissionCreationValidatorInterface = field(default_factory=SubmissionCreationValidator)
    ownership_guard: SubmissionOwnershipGuard = field(default_factory=SubmissionOwnershipGuardImpl)

    def create_submission(self, request: SubmissionCreationRequest, homework: Homework, user) -> HomeworkSubmission:
        """Create a new submission with full validation"""
        # Validate role (only students can create submissions)
        if user.role != UserRole.STUDENT.value:
            raise ValidationError(ErrorMessages.USER_MUST_BE_STUDENT.value)
        
        # Validate that user is a student enrolled in the course
        course = homework.lecture.course
        if not course.students.filter(id=user.id).exists():
            raise ValidationError(ErrorMessages.STUDENT_NOT_ENROLLED.value)

        # Validate request
        validation_result = self.validation_service.validate_submission_creation(request, homework, user.id)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._create_submission_with_validation(request, homework, user)

    @transaction.atomic
    def _create_submission_with_validation(self, request: SubmissionCreationRequest, homework: Homework, user) -> HomeworkSubmission:
        """Create submission in a transaction"""
        return HomeworkSubmission.objects.create(
            homework=homework,
            student=user,
            content=request.content
        )


@dataclass
class SubmissionUpdateService:
    """Handles submission updates with validation and business logic"""
    validation_service: SubmissionUpdateValidatorInterface = field(default_factory=SubmissionUpdateValidator)
    ownership_guard: SubmissionOwnershipGuard = field(default_factory=SubmissionOwnershipGuardImpl)

    def update_submission(self, instance: HomeworkSubmission, request: SubmissionUpdateRequest, user) -> HomeworkSubmission:
        """Update an existing submission with full validation"""
        # Validate ownership
        self.ownership_guard.ensure_owner(instance, user)

        # Validate request
        validation_result = self.validation_service.validate_submission_update(request, instance)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._update_submission_with_validation(instance, request)

    @transaction.atomic
    def _update_submission_with_validation(self, instance: HomeworkSubmission, request: SubmissionUpdateRequest) -> HomeworkSubmission:
        """Update submission in a transaction"""
        if request.content is not None:
            instance.content = request.content
        if request.is_submitted is not None:
            instance.is_submitted = request.is_submitted

        instance.save()
        return instance


@dataclass
class SubmissionManagementService(SubmissionService):
    """Composite service that handles all submission operations"""
    creation_service: SubmissionCreationService = field(default_factory=SubmissionCreationService)
    update_service: SubmissionUpdateService = field(default_factory=SubmissionUpdateService)
    ownership_guard: SubmissionOwnershipGuard = field(default_factory=SubmissionOwnershipGuardImpl)

    def create(self, *, homework, user, validated_data) -> HomeworkSubmission:
        """Create a new submission"""
        request = SubmissionCreationRequest(
            content=validated_data[ModelFields.CONTENT.value],
            homework_id=homework.id
        )
        return self.creation_service.create_submission(request, homework, user)

    def update(self, *, instance, user, validated_data, partial=False) -> HomeworkSubmission:
        """Update an existing submission"""
        request = SubmissionUpdateRequest(
            entity_id=instance.id,
            content=validated_data.get(ModelFields.CONTENT.value),
            is_submitted=validated_data.get(ModelFields.IS_SUBMITTED.value)
        )
        return self.update_service.update_submission(instance, request, user)

    def delete(self, *, instance, user) -> None:
        """Delete a submission"""
        self.ownership_guard.ensure_owner(instance, user)
        instance.delete()

    def get_filtered_submissions(self, *, homework_id, user):
        """Get submissions filtered by user role and permissions"""
        from apps.homeworks.models import HomeworkSubmission
        from common.enums import UserRole
        
        queryset = (
            HomeworkSubmission.objects
            .select_related(
                ModelFields.HOMEWORK.value,
                f"{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}",
                f"{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}__{ModelFields.COURSE.value}",
                f"{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}__{ModelFields.COURSE.value}__{ModelFields.PRIMARY_OWNER.value}",
                ModelFields.STUDENT.value,
            )
            .filter(homework_id=homework_id)
        )
        
        # If user is a student, only show their own submissions
        if user.role == UserRole.STUDENT.value:
            queryset = queryset.filter(student_id=user.id)
        
        # If user is a teacher, show all submissions (they can see everyone's)
        # This is handled by the ownership guard for individual operations
        
        return queryset
