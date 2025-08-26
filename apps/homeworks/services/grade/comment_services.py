from dataclasses import dataclass
from rest_framework.exceptions import PermissionDenied

from apps.homeworks.models import GradeComment
from apps.homeworks.services.protocols import GradeCommentService
from common.enums import ErrorMessages, ModelFields


@dataclass
class GradeCommentManagementService(GradeCommentService):
    def _ensure_can_view(self, *, grade, user) -> None:
        if not user or not user.is_authenticated:
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)
        submission = grade.submission
        course = submission.homework.lecture.course
        is_owner_student = submission.student_id == user.id
        is_teacher = course.primary_owner_id == user.id or course.teachers.filter(id=user.id).exists()
        if not (is_owner_student or is_teacher):
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

    def _ensure_can_comment(self, *, grade, user) -> None:
        # Same rule as view
        self._ensure_can_view(grade=grade, user=user)

    def list(self, *, grade, user):
        self._ensure_can_view(grade=grade, user=user)
        return GradeComment.objects.filter(grade=grade).select_related(ModelFields.AUTHOR.value)

    def create(self, *, grade, user, validated_data):
        self._ensure_can_comment(grade=grade, user=user)
        return GradeComment.objects.create(
            grade=grade,
            author=user,
            comment=validated_data[ModelFields.COMMENT.value]
        )
