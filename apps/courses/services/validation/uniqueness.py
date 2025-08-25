from rest_framework.exceptions import ValidationError
from apps.courses.models import Course
from common.enums import ErrorMessages
from .interfaces import CourseUniquenessValidatorInterface


class CourseUniquenessValidator(CourseUniquenessValidatorInterface):
    """Concrete implementation for course uniqueness validation"""

    def validate_course_uniqueness(self, name: str, primary_owner_id: int) -> None:
        """Validate that course name is unique for the given teacher"""
        if Course.objects.filter(name=name, primary_owner_id=primary_owner_id).exists():
            raise ValidationError(ErrorMessages.COURSE_ALREADY_EXISTS_FOR_TEACHER.value)

    def validate_course_uniqueness_for_update(self, course_id: int, name: str, primary_owner_id: int) -> None:
        """Validate that course name is unique for the given teacher during update"""
        existing_course = Course.objects.filter(
            name=name,
            primary_owner_id=primary_owner_id
        ).exclude(id=course_id).first()

        if existing_course:
            raise ValidationError(ErrorMessages.COURSE_ALREADY_EXISTS_FOR_TEACHER.value)
