from dataclasses import dataclass, field
from typing import List, Optional
from rest_framework.exceptions import ValidationError

from common.enums import UserRole, FieldDisplayNames
from apps.courses.services.dtos import CourseUpdateRequest, CourseUpdateValidationResult, UserValidationResult
from .interfaces import CourseUpdateValidatorInterface, CourseUniquenessValidatorInterface, \
    BusinessRuleValidatorInterface
from .uniqueness import CourseUniquenessValidator
from .business_rules import BusinessRuleValidator
from .base import BaseValidator


@dataclass
class UpdateValidationContext:
    """Context object to pass validation state between pipeline steps"""
    request: CourseUpdateRequest
    errors: List[str] = field(default_factory=list)
    primary_owner: Optional[UserValidationResult] = None
    teachers: Optional[List[UserValidationResult]] = None
    students: Optional[List[UserValidationResult]] = None


@dataclass
class CourseUpdateValidator(BaseValidator, CourseUpdateValidatorInterface):
    """SOLID-compliant orchestrator using validation pipeline pattern"""

    uniqueness_validator: CourseUniquenessValidatorInterface = field(default_factory=CourseUniquenessValidator)
    business_rule_validator: BusinessRuleValidatorInterface = field(default_factory=BusinessRuleValidator)

    def validate_course_update(self, request: CourseUpdateRequest) -> CourseUpdateValidationResult:
        context = UpdateValidationContext(request=request)

        self._validate_basic_fields(context)
        self._validate_primary_owner_if_provided(context)
        self._validate_teachers_if_provided(context)
        self._validate_students_if_provided(context)
        self._validate_business_rules_for_update(context)

        return self._build_result(context)

    def _validate_basic_fields(self, context: UpdateValidationContext) -> None:
        try:
            self.business_rule_validator.validate_course_id(context.request.course_id)
            self.business_rule_validator.validate_course_name_for_update(context.request.name)
            self.business_rule_validator.validate_primary_owner_id_for_update(context.request.primary_owner_id)
        except ValidationError as e:
            error_msg = self._extract_clean_error_message(e)
            context.errors.append(error_msg)

    def _validate_primary_owner_if_provided(self, context: UpdateValidationContext) -> None:
        if context.request.primary_owner_id is not None:
            try:
                context.primary_owner = self.user_role_validator.validate_user_role(
                    context.request.primary_owner_id, UserRole.TEACHER
                )
            except ValidationError as e:
                error_msg = self._extract_clean_error_message(e)
                context.errors.append(f"{FieldDisplayNames.PRIMARY_OWNER.value}: {error_msg}")

    def _validate_teachers_if_provided(self, context: UpdateValidationContext) -> None:
        context.teachers = self._validate_user_roles_if_provided(
            user_ids=context.request.teacher_ids,
            role=UserRole.TEACHER,
            role_name=FieldDisplayNames.TEACHER.value,
            context=context
        )

    def _validate_students_if_provided(self, context: UpdateValidationContext) -> None:
        context.students = self._validate_user_roles_if_provided(
            user_ids=context.request.student_ids,
            role=UserRole.STUDENT,
            role_name=FieldDisplayNames.STUDENT.value,
            context=context
        )

    def _validate_user_roles_if_provided(
            self,
            user_ids: Optional[List[int]],
            role: UserRole,
            role_name: str,
            context: UpdateValidationContext
    ) -> Optional[List[UserValidationResult]]:
        if user_ids is None:
            return None

        return self._validate_user_roles_with_errors(
            user_ids=user_ids,
            role=role,
            role_name=role_name,
            errors=context.errors
        )

    def _validate_business_rules_for_update(self, context: UpdateValidationContext) -> None:
        try:
            if context.request.name is not None:
                primary_owner_id = context.request.primary_owner_id
                if primary_owner_id is None:
                    from apps.courses.models import Course
                    current_course = Course.objects.get(id=context.request.course_id)
                    primary_owner_id = current_course.primary_owner_id
                
                self.uniqueness_validator.validate_course_uniqueness_for_update(
                    context.request.course_id, context.request.name, primary_owner_id
                )

            if (context.request.primary_owner_id is not None and
                    context.request.teacher_ids is not None and
                    context.request.primary_owner_id in context.request.teacher_ids):
                self.business_rule_validator.validate_primary_owner_not_in_teachers(
                    context.request.primary_owner_id, context.request.teacher_ids
                )
        except ValidationError as e:
            error_msg = self._extract_clean_error_message(e)
            context.errors.append(error_msg)

    def _build_result(self, context: UpdateValidationContext) -> CourseUpdateValidationResult:
        return CourseUpdateValidationResult(
            primary_owner=context.primary_owner,
            teachers=context.teachers,
            students=context.students,
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )
