from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any
from django.contrib.auth import get_user_model
from common.enums import SuccessMessages, UserFields, ResponseKeys
from apps.users.serializers import UserRegistrationSerializer
from apps.users.services.authentication import AuthTokenService

User = get_user_model()


@dataclass
class RegistrationResult:
    user: Optional[Any] = None
    errors: Optional[Dict[str, Any]] = None

    @property
    def is_success(self) -> bool:
        return self.user is not None and self.errors is None


@dataclass
class UserResponseData:
    id: int
    email: str
    first_name: str
    last_name: str
    role: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            UserFields.ID.value: self.id,
            UserFields.EMAIL.value: self.email,
            UserFields.FIRST_NAME.value: self.first_name,
            UserFields.LAST_NAME.value: self.last_name,
            UserFields.ROLE.value: self.role,
        }


@dataclass
class RegistrationResponse:
    message: str
    user: UserResponseData
    tokens: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            ResponseKeys.MESSAGE.value: self.message,
            ResponseKeys.USER.value: self.user.to_dict(),
            ResponseKeys.TOKENS.value: self.tokens,
        }


class UserRegistrationService:

    @staticmethod
    def register_user(data) -> RegistrationResult:
        serializer = UserRegistrationSerializer(data=data)

        if not serializer.is_valid():
            return RegistrationResult(errors=serializer.errors)

        validated_data = serializer.validated_data
        validated_data.pop(UserFields.PASSWORD_CONFIRM.value, None)

        user = User.objects.create_user(**validated_data)
        return RegistrationResult(user=user)


class ResponseBuilderService:

    @staticmethod
    def build_user_response_data(user) -> UserResponseData:
        return UserResponseData(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role
        )

    @staticmethod
    def build_registration_response(user, tokens: Dict[str, str]) -> RegistrationResponse:
        user_data = ResponseBuilderService.build_user_response_data(user)
        return RegistrationResponse(
            message=SuccessMessages.REGISTRATION_SUCCESS.value,
            user=user_data,
            tokens=tokens
        )


class RegistrationWithTokensService:

    @staticmethod
    def execute(data) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        registration_result = UserRegistrationService.register_user(data)

        if not registration_result.is_success:
            return None, registration_result.errors

        tokens = AuthTokenService.generate_tokens_for_user(registration_result.user)

        response = ResponseBuilderService.build_registration_response(
            registration_result.user,
            tokens
        )

        return response.to_dict(), None
