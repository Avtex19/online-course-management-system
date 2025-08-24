from dataclasses import dataclass
from django.contrib.auth import get_user_model

from common.enums import UserRole

User = get_user_model()


@dataclass(frozen=True)
class UserValidationResult:
    user_id: int
    user: User
    role: UserRole
