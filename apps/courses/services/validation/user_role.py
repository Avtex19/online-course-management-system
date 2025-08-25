from dataclasses import dataclass, field
from rest_framework.exceptions import ValidationError
from common.enums import UserRole
from apps.courses.services.dtos import UserValidationResult
from apps.courses.services.user import UserService
from .interfaces import UserRoleValidatorInterface


@dataclass
class UserRoleValidator(UserRoleValidatorInterface):

    user_service: UserService = field(default_factory=UserService)

    def validate_user_role(self, user_id: int, role: UserRole) -> UserValidationResult:
        """Validate that user exists and has the required role"""
        try:
            user = self.user_service.get_user_by_role_or_raise(user_id, role=role)
            return UserValidationResult(user_id=user_id, user=user, role=role)
        except ValidationError as e:
            raise ValidationError(e.detail)
