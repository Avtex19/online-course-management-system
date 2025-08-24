from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from common.enums import UserRole, UserFields, ErrorMessages

User = get_user_model()


class UserService:
    @staticmethod
    def get_user_by_role_or_raise(user_id: int, role: UserRole) -> User:
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValidationError(ErrorMessages.USER_DOESNT_EXIST.value)

        if getattr(user, UserFields.ROLE.value) != role.value:
            if role == UserRole.TEACHER:
                raise ValidationError(ErrorMessages.USER_MUST_BE_TEACHER.value)
            elif role == UserRole.STUDENT:
                raise ValidationError(ErrorMessages.USER_MUST_BE_STUDENT.value)
        return user