from dataclasses import dataclass, field
from typing import List
from rest_framework.exceptions import ValidationError

from common.enums import UserRole
from apps.courses.services.dtos import UserValidationResult
from .interfaces import UserRoleValidatorInterface
from .user_role import UserRoleValidator


@dataclass
class BaseValidator:
    """Base validator class with shared user validation logic (DRY principle)"""
    
    user_role_validator: UserRoleValidatorInterface = field(default_factory=UserRoleValidator)
    
    def _validate_user_roles_with_errors(
        self,
        user_ids: List[int],
        role: UserRole,
        role_name: str,
        errors: List[str]
    ) -> List[UserValidationResult]:
        """
        Generic helper to validate user roles and collect errors.
        
        Returns:
            List of successfully validated users
        
        Side effects:
            Adds error messages to the errors list for failed validations
        """
        validated_users = []
        for user_id in user_ids:
            try:
                user = self.user_role_validator.validate_user_role(user_id, role)
                validated_users.append(user)
            except ValidationError as e:
                error_msg = str(e.detail[0]) if hasattr(e, 'detail') and e.detail else str(e)
                errors.append(f"{role_name} {user_id}: {error_msg}")
        
        return validated_users
    
    def _extract_clean_error_message(self, validation_error: ValidationError) -> str:
        """Extract clean error message without ErrorDetail wrapper"""
        return str(validation_error.detail[0]) if hasattr(validation_error, 'detail') and validation_error.detail else str(validation_error)
