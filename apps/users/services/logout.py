from dataclasses import dataclass, field
from typing import Optional, Tuple, Dict, Any
from apps.users.serializers import LogoutSerializer
from apps.users.services.token_blacklist import (
    TokenBlacklistService,
    AccessTokenBlacklistService,
)
from common.enums import SuccessMessages, AuthHeaders, TokenFields, ResponseKeys, ErrorMessages


@dataclass
class TokenExtractionResult:
    refresh_token: str
    access_token: Optional[str] = None

    @property
    def has_access_token(self) -> bool:
        return self.access_token is not None


@dataclass
class BlacklistResult:
    success: bool
    error: Optional[str] = None

    @property
    def failed(self) -> bool:
        return not self.success


@dataclass
class LogoutErrors:
    errors: Dict[str, str] = field(default_factory=dict)

    def add_refresh_error(self, error: str) -> None:
        self.errors[TokenFields.REFRESH.value] = ErrorMessages.INVALID_TOKEN.value.format(error=error)

    def add_access_error(self, error: str) -> None:
        self.errors[TokenFields.ACCESS.value] = ErrorMessages.INVALID_TOKEN.value.format(error=error)

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)

    def to_dict(self) -> Dict[str, str]:
        return self.errors


@dataclass
class LogoutResponse:
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {ResponseKeys.MESSAGE.value: self.message}


class TokenExtractionService:

    @staticmethod
    def extract_tokens(validated_data: Dict[str, Any], request=None) -> TokenExtractionResult:
        refresh_token = validated_data[TokenFields.REFRESH.value]
        access_token = validated_data.get(TokenFields.ACCESS.value)

        if not access_token and request is not None:
            access_token = TokenExtractionService._extract_from_header(request)

        return TokenExtractionResult(
            refresh_token=refresh_token,
            access_token=access_token
        )

    @staticmethod
    def _extract_from_header(request) -> Optional[str]:
        auth_header = request.headers.get(AuthHeaders.AUTH_HEADER.value) or request.META.get(
            AuthHeaders.AUTH_HEADER_FALLBACK.value
        )

        if auth_header and auth_header.startswith(AuthHeaders.BEARER_PREFIX.value):
            return auth_header.split(' ', 1)[1].strip()

        return None


class LogoutService:

    @staticmethod
    def execute(data, request=None) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, str]]]:
        serializer = LogoutSerializer(data=data)
        if not serializer.is_valid():
            return None, serializer.errors

        tokens = TokenExtractionService.extract_tokens(serializer.validated_data, request)

        logout_errors = LogoutService._process_token_blacklisting(tokens)

        if logout_errors.has_errors:
            return None, logout_errors.to_dict()

        response = LogoutResponse(message=SuccessMessages.LOGOUT_SUCCESS.value)
        return response.to_dict(), None

    @staticmethod
    def _process_token_blacklisting(tokens: TokenExtractionResult) -> LogoutErrors:
        errors = LogoutErrors()

        refresh_result = LogoutService._blacklist_refresh_token(tokens.refresh_token)
        if refresh_result.failed:
            errors.add_refresh_error(refresh_result.error)

        if tokens.has_access_token:
            access_result = LogoutService._blacklist_access_token(tokens.access_token)
            if access_result.failed:
                errors.add_access_error(access_result.error)

        return errors

    @staticmethod
    def _blacklist_refresh_token(refresh_token: str) -> BlacklistResult:
        result = TokenBlacklistService.blacklist_refresh_token(refresh_token)
        return BlacklistResult(success=result.success, error=result.error)

    @staticmethod
    def _blacklist_access_token(access_token: str) -> BlacklistResult:
        result = AccessTokenBlacklistService.blacklist(access_token)
        return BlacklistResult(success=result.success, error=result.error)