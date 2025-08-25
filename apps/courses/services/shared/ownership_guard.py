from dataclasses import dataclass
from rest_framework.exceptions import PermissionDenied

from apps.courses.services.protocols import OwnershipGuard
from common.enums import ErrorMessages


@dataclass
class CourseOwnershipGuard(OwnershipGuard):

    def ensure_owner(self, course, user) -> None:
        if not user or not user.is_authenticated:
            raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)

        if course.primary_owner_id == user.id:
            return

        if course.teachers.filter(id=user.id).exists():
            return

        raise PermissionDenied(ErrorMessages.COURSE_ACCESS_DENIED.value)
