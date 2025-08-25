from dataclasses import dataclass, field
from typing import List
from rest_framework.exceptions import ValidationError

from common.enums import UserRole, FieldDisplayNames
from apps.courses.services.dtos import CourseCreationRequest, CourseValidationResult, UserValidationResult
from .interfaces import CourseCreationValidatorInterface,  CourseUniquenessValidatorInterface, BusinessRuleValidatorInterface
from .uniqueness import CourseUniquenessValidator
from .business_rules import BusinessRuleValidator
from .base import BaseValidator


@dataclass
class ValidationContext:
    """Context object to pass validation state between pipeline steps"""
    request: CourseCreationRequest
    errors: List[str] = field(default_factory=list)
    primary_owner: UserValidationResult = None
    teachers: List[UserValidationResult] = field(default_factory=list)
    students: List[UserValidationResult] = field(default_factory=list)


@dataclass
class CourseCreationValidator(BaseValidator, CourseCreationValidatorInterface):

    uniqueness_validator: CourseUniquenessValidatorInterface = field(default_factory=CourseUniquenessValidator)
    business_rule_validator: BusinessRuleValidatorInterface = field(default_factory=BusinessRuleValidator)
    
    def validate_course_creation(self, request: CourseCreationRequest) -> CourseValidationResult:
        context = ValidationContext(request=request)
        
        self._validate_basic_fields(context)
        self._validate_primary_owner(context)
        self._validate_teachers(context)
        self._validate_students(context)
        self._validate_business_rules(context)
        
        return self._build_result(context)
    
    def _validate_basic_fields(self, context: ValidationContext) -> None:
        try:
            self.business_rule_validator.validate_course_name(context.request.name)
            self.business_rule_validator.validate_primary_owner_id(context.request.primary_owner_id)
        except ValidationError as e:
            error_msg = self._extract_clean_error_message(e)
            context.errors.append(error_msg)
    
    def _validate_primary_owner(self, context: ValidationContext) -> None:
        try:
            context.primary_owner = self.user_role_validator.validate_user_role(
                context.request.primary_owner_id, UserRole.TEACHER
            )
        except ValidationError as e:
            error_msg = self._extract_clean_error_message(e)
            context.errors.append(f"{FieldDisplayNames.PRIMARY_OWNER.value}: {error_msg}")
    
    def _validate_teachers(self, context: ValidationContext) -> None:
        self._validate_user_roles(
            user_ids=context.request.teacher_ids,
            role=UserRole.TEACHER,
            role_name=FieldDisplayNames.TEACHER.value,
            target_list=context.teachers,
            context=context
        )
    
    def _validate_students(self, context: ValidationContext) -> None:
        self._validate_user_roles(
            user_ids=context.request.student_ids,
            role=UserRole.STUDENT,
            role_name=FieldDisplayNames.STUDENT.value,
            target_list=context.students,
            context=context
        )
    
    def _validate_user_roles(
        self, 
        user_ids: List[int], 
        role: UserRole, 
        role_name: str,
        target_list: List[UserValidationResult],
        context: ValidationContext
    ) -> None:
        """Validate user roles and append successful results to target_list (DRY: uses shared logic)"""
        validated_users = self._validate_user_roles_with_errors(
            user_ids=user_ids,
            role=role,
            role_name=role_name,
            errors=context.errors
        )
        target_list.extend(validated_users)
    
    def _validate_business_rules(self, context: ValidationContext) -> None:
        try:
            self.uniqueness_validator.validate_course_uniqueness(
                context.request.name, context.request.primary_owner_id
            )
            self.business_rule_validator.validate_primary_owner_not_in_teachers(
                context.request.primary_owner_id, context.request.teacher_ids
            )
        except ValidationError as e:
            error_msg = self._extract_clean_error_message(e)
            context.errors.append(error_msg)
    
    def _build_result(self, context: ValidationContext) -> CourseValidationResult:
        return CourseValidationResult(
            primary_owner=context.primary_owner,
            teachers=context.teachers,
            students=context.students,
            is_valid=len(context.errors) == 0,
            errors=context.errors
        )
