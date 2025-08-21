from typing import Optional, Tuple, Dict

from apps.users.serializers import LogoutSerializer
from apps.users.services.token_blacklist import (
    TokenBlacklistService,
    AccessTokenBlacklistService,
)
from common.enums import SuccessMessages,AuthHeaders,TokenFields,ResponseKeys


class LogoutService:

    @staticmethod
    def execute(data, request=None) -> Tuple[Optional[dict], Optional[Dict[str, str]]]:

        serializer = LogoutSerializer(data=data)

        if not serializer.is_valid():
            return None, serializer.errors

        validated_data = serializer.validated_data
        refresh_token = validated_data[TokenFields.REFRESH.value]

        errors: Dict[str, str] = {}
        success, error = TokenBlacklistService.blacklist_refresh_token(refresh_token)
        if not success:
            errors[TokenFields.REFRESH.value] = f"Invalid token: {error}"

        # Prefer access token from body if provided; otherwise from Authorization header
        access_token_str = validated_data.get(TokenFields.ACCESS.value)
        if not access_token_str and request is not None:
            auth_header = request.headers.get(AuthHeaders.AUTH_HEADER.value) or request.META.get(AuthHeaders.AUTH_HEADER_FALLBACK.value)
            if auth_header and auth_header.startswith(AuthHeaders.BEARER_PREFIX.value):
                access_token_str = auth_header.split(' ', 1)[1].strip()

        if access_token_str:
            success_access, error_access = AccessTokenBlacklistService.blacklist(access_token_str)
            if not success_access:
                errors[TokenFields.ACCESS.value] = f"Invalid token: {error_access}"

        if not errors:
            return {ResponseKeys.MESSAGE.value: SuccessMessages.LOGOUT_SUCCESS}, None

        return None, errors
