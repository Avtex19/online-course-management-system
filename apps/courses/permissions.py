from rest_framework.permissions import BasePermission
from common.enums import ErrorMessages


class IsCoursePrimaryOwner(BasePermission):
    """Allows access only to the primary owner of the course instance."""

    message = ErrorMessages.ONLY_PRIMARY_OWNER_ALLOWED.value

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and obj.primary_owner_id == user.id)



