from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import UserLoginSerializer
from common.enums import ErrorMessages, ResponseKeys, SuccessMessages, TokenFields, UserFields, ValidationFields

User = get_user_model()


@dataclass
class AuthResult:
    user: Optional[User] = None
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.user is not None and self.error is None


@dataclass
class TokenData:
    access: str
    refresh: str

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class UserData:
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    last_login: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoginResponse:
    message: str
    user: UserData
    tokens: TokenData

    def to_dict(self) -> Dict[str, Any]:
        return {
            ResponseKeys.MESSAGE.value: self.message,
            ResponseKeys.USER.value: self.user.to_dict(),
            ResponseKeys.TOKENS.value: self.tokens.to_dict()
        }


class UserAuthenticationService:

    @staticmethod
    def authenticate_user(email: str, password: str) -> AuthResult:
        if not email or not password:
            return AuthResult(error=ErrorMessages.INVALID_CREDENTIALS.value)

        user = authenticate(email=email, password=password)
        if not user:
            return AuthResult(error=ErrorMessages.INVALID_CREDENTIALS.value)

        if not user.is_active:
            return AuthResult(error=ErrorMessages.INACTIVE_ACCOUNT.value)

        return AuthResult(user=user)

    @staticmethod
    def update_last_login(user: User) -> None:
        user.last_login = timezone.now()
        user.save(update_fields=[UserFields.LAST_LOGIN.value])


class AuthTokenService:

    @staticmethod
    def generate_tokens_for_user(user: User) -> Dict[str, str]:
        refresh = RefreshToken.for_user(user)
        return {
            TokenFields.ACCESS_SHORT.value: str(refresh.access_token),
            TokenFields.REFRESH_SHORT.value: str(refresh)
        }


class ResponseBuilderService:

    @staticmethod
    def build_user_data(user: User) -> UserData:
        return UserData(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            last_login=user.last_login
        )

    @staticmethod
    def build_login_response(user: User, tokens: Dict[str, str]) -> Dict[str, Any]:
        user_data = ResponseBuilderService.build_user_data(user)
        return {
            ResponseKeys.MESSAGE.value: SuccessMessages.LOGIN_SUCCESS.value,
            ResponseKeys.USER.value: user_data.to_dict(),
            ResponseKeys.TOKENS.value: tokens
        }


class LoginWithTokensService:

    @staticmethod
    def execute(data) -> tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        serializer = UserLoginSerializer(data=data)
        if not serializer.is_valid():
            return None, serializer.errors

        validated_data = serializer.validated_data

        auth_result = UserAuthenticationService.authenticate_user(
            validated_data.get(UserFields.EMAIL.value),
            validated_data.get(UserFields.PASSWORD.value)
        )

        if not auth_result.is_success:
            return None, {ValidationFields.NON_FIELD_ERRORS.value: [auth_result.error]}

        UserAuthenticationService.update_last_login(auth_result.user)

        tokens = AuthTokenService.generate_tokens_for_user(auth_result.user)

        response_data = ResponseBuilderService.build_login_response(auth_result.user, tokens)

        return response_data, None
