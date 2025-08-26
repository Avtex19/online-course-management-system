from dataclasses import dataclass
from rest_framework.exceptions import PermissionDenied

from apps.homeworks.services.protocols import HomeworkOwnershipGuard, SubmissionOwnershipGuard, GradeOwnershipGuard
from common.enums import ErrorMessages, UserRole


@dataclass
class HomeworkOwnershipGuardImpl(HomeworkOwnershipGuard):
    """Guards ownership for homework-related operations"""

    def ensure_owner(self, homework, user) -> None:
        if not user or not user.is_authenticated:
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        if user.role != UserRole.TEACHER.value:
            raise PermissionDenied(ErrorMessages.USER_MUST_BE_TEACHER.value)

        if homework.created_by_id == user.id:
            return

        course = homework.lecture.course
        if course.primary_owner_id == user.id:
            return

        if course.teachers.filter(id=user.id).exists():
            return

        raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)


@dataclass
class SubmissionOwnershipGuardImpl(SubmissionOwnershipGuard):
    """Guards ownership for submission-related operations"""

    def ensure_owner(self, submission, user) -> None:
        if not user or not user.is_authenticated:
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        if submission.student_id == user.id:
            return

        homework = submission.homework
        if homework.created_by_id == user.id:
            return

        course = homework.lecture.course
        if course.primary_owner_id == user.id:
            return

        if course.teachers.filter(id=user.id).exists():
            return

        raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)


@dataclass
class GradeOwnershipGuardImpl(GradeOwnershipGuard):
    """Guards ownership for grade-related operations"""

    def ensure_owner(self, grade, user) -> None:
        if not user or not user.is_authenticated:
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        if grade.graded_by_id == user.id:
            return

        submission = grade.submission
        homework = submission.homework
        course = homework.lecture.course
        
        if course.primary_owner_id == user.id:
            return

        if course.teachers.filter(id=user.id).exists():
            return

        raise PermissionDenied(ErrorMessages.ONLY_GRADED_BY_TEACHER_CAN_UPDATE.value)
