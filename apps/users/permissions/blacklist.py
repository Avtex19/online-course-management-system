from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from common.enums import ErrorMessages, TokenFields


class DenyBlacklistedToken(BasePermission):
    message = ErrorMessages.TOKEN_BLACKLISTED.value

    def has_permission(self, request: Request, view: View):
        if not request.user or not request.auth:
            return True

        try:
            jti = request.auth.get(TokenFields.JTI.value) if hasattr(request.auth, 'get') else request.auth[
                TokenFields.JTI.value]
        except Exception:
            self.message = ErrorMessages.TOKEN_MISSING_JTI.value
            return True

        if not jti:
            return True

        try:
            outstanding = OutstandingToken.objects.get(jti=jti)
        except OutstandingToken.DoesNotExist:
            self.message = ErrorMessages.TOKEN_NOT_TRACKED.value
            return True

        is_blacklisted = BlacklistedToken.objects.filter(token=outstanding).exists()
        if is_blacklisted:
            self.message = ErrorMessages.TOKEN_BLACKLISTED.value
            return False

        return True
