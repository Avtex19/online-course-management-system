from dataclasses import dataclass, field
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.homeworks.services.grade.dtos import GradeCreationRequest, GradeUpdateRequest
from apps.homeworks.services.grade.validation import GradeCreationValidator, GradeUpdateValidator
from apps.homeworks.services.validation.interfaces import GradeCreationValidatorInterface, GradeUpdateValidatorInterface
from apps.homeworks.services.shared.ownership_guard import GradeOwnershipGuardImpl
from apps.homeworks.services.protocols import GradeOwnershipGuard, GradeService
from common.enums import ModelFields, UserRole, ErrorMessages
from apps.homeworks.models import HomeworkGrade, HomeworkSubmission
from rest_framework.exceptions import PermissionDenied

@dataclass
class GradeCreationService:
    """Handles grade creation with validation and business logic"""
    validation_service: GradeCreationValidatorInterface = field(default_factory=GradeCreationValidator)
    ownership_guard: GradeOwnershipGuard = field(default_factory=GradeOwnershipGuardImpl)

    def create_grade(self, request: GradeCreationRequest, user) -> HomeworkGrade:
        """Create a new grade with full validation"""
        # Validate role (only teachers can create grades)
        if user.role != UserRole.TEACHER.value:
            raise ValidationError(ErrorMessages.ONLY_TEACHERS_CAN_GRADE.value)

        # Validate request
        validation_result = self.validation_service.validate_grade_creation(request, user.id)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._create_grade_with_validation(request, user)

    @transaction.atomic
    def _create_grade_with_validation(self, request: GradeCreationRequest, user) -> HomeworkGrade:
        """Create grade in a transaction"""
        submission = HomeworkSubmission.objects.get(id=request.submission_id)
        return HomeworkGrade.objects.create(
            submission=submission,
            grade=request.grade,
            comments=request.comments,
            graded_by=user
        )


@dataclass
class GradeUpdateService:
    """Handles grade updates with validation and business logic"""
    validation_service: GradeUpdateValidatorInterface = field(default_factory=GradeUpdateValidator)
    ownership_guard: GradeOwnershipGuard = field(default_factory=GradeOwnershipGuardImpl)

    def update_grade(self, instance: HomeworkGrade, request: GradeUpdateRequest, user) -> HomeworkGrade:
        """Update an existing grade with full validation"""
        # Validate ownership (only the teacher who graded can update)
        self.ownership_guard.ensure_owner(instance, user)

        # Validate request
        validation_result = self.validation_service.validate_grade_update(request, instance)

        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)

        return self._update_grade_with_validation(instance, request)

    @transaction.atomic
    def _update_grade_with_validation(self, instance: HomeworkGrade, request: GradeUpdateRequest) -> HomeworkGrade:
        """Update grade in a transaction"""
        if request.grade is not None:
            instance.grade = request.grade
        if request.comments is not None:
            instance.comments = request.comments

        instance.save()
        return instance


@dataclass
class GradeManagementService(GradeService):
    """Composite service that handles all grade operations"""
    creation_service: GradeCreationService = field(default_factory=GradeCreationService)
    update_service: GradeUpdateService = field(default_factory=GradeUpdateService)
    ownership_guard: GradeOwnershipGuard = field(default_factory=GradeOwnershipGuardImpl)

    def create(self, *, submission, user, validated_data) -> HomeworkGrade:
        """Create a new grade"""
        request = GradeCreationRequest(
            submission_id=submission.id,
            grade=validated_data.get(ModelFields.GRADE.value),
            comments=validated_data.get(ModelFields.COMMENTS.value, "")
        )
        return self.creation_service.create_grade(request, user)

    def update(self, *, instance, user, validated_data, partial=False) -> HomeworkGrade:
        """Update an existing grade"""
        request = GradeUpdateRequest(
            grade_id=instance.id,
            grade=validated_data.get(ModelFields.GRADE.value),
            comments=validated_data.get(ModelFields.COMMENTS.value)
        )
        return self.update_service.update_grade(instance, request, user)

    def delete(self, *, instance, user) -> None:
        """Delete a grade"""
        self.ownership_guard.ensure_owner(instance, user)
        instance.delete()

    def get_grades_for_submission(self, *, submission_id, user):
        """Get grades for a specific submission"""
        

        if not user or not user.is_authenticated:
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        # Load submission and course to authorize access
        try:
            submission = HomeworkSubmission.objects.select_related(
                ModelFields.HOMEWORK.value,
                f"{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}",
                f"{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}__{ModelFields.COURSE.value}",
            ).get(id=submission_id)
        except HomeworkSubmission.DoesNotExist:
            # Mirror list behavior for nonexistent submission
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        course = submission.homework.lecture.course

        # Check if user is a teacher (teachers can always access)
        is_teacher = (
            course.primary_owner_id == user.id or
            course.teachers.filter(id=user.id).exists()
        )

        if is_teacher:
            # Teachers can always access grades
            queryset = (
                HomeworkGrade.objects
                .select_related(
                    f"{ModelFields.SUBMISSION.value}__{ModelFields.HOMEWORK.value}",
                    f"{ModelFields.SUBMISSION.value}__{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}",
                    f"{ModelFields.SUBMISSION.value}__{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}__{ModelFields.COURSE.value}",
                    ModelFields.GRADED_BY.value,
                )
                .filter(submission_id=submission_id)
            )
            return queryset

        # For students, check both ownership AND current enrollment
        is_owner = submission.student_id == user.id
        is_enrolled = course.students.filter(id=user.id).exists()

        # Only the submission owner who is still enrolled may view grades
        if not (is_owner and is_enrolled):
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        queryset = (
            HomeworkGrade.objects
            .select_related(
                f"{ModelFields.SUBMISSION.value}__{ModelFields.HOMEWORK.value}",
                f"{ModelFields.SUBMISSION.value}__{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}",
                f"{ModelFields.SUBMISSION.value}__{ModelFields.HOMEWORK.value}__{ModelFields.LECTURE.value}__{ModelFields.COURSE.value}",
                ModelFields.GRADED_BY.value,
            )
            .filter(submission_id=submission_id)
        )

        return queryset
