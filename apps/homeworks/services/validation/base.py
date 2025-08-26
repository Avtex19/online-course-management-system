from dataclasses import dataclass, field
from rest_framework.exceptions import ValidationError

from common.enums import ValidationFields
from apps.courses.services.validation.interfaces import UserRoleValidatorInterface
from apps.courses.services.validation.user_role import UserRoleValidator


@dataclass
class BaseValidator:
    """Base validator class with shared validation logic (DRY principle)"""
    user_role_validator: UserRoleValidatorInterface = field(default_factory=UserRoleValidator)
    
    def _extract_clean_error_message(self, validation_error: ValidationError) -> str:
        """Extract clean error message without ErrorDetail wrapper"""
        return str(validation_error.detail[0]) if hasattr(validation_error, ValidationFields.DETAIL.value) and validation_error.detail else str(validation_error)
