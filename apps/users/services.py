from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegistrationSerializer, UserLoginSerializer, LogoutSerializer
from common.enums import ErrorMessages, SuccessMessages

User = get_user_model()


class UserRegistrationService:
    @staticmethod
    def register_user(data):
        serializer = UserRegistrationSerializer(data=data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data.pop("password_confirm", None)
            user = User.objects.create_user(**validated_data)
            return user, None

        return None, serializer.errors


class AuthTokenService:

    @staticmethod
    def generate_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class RegistrationWithTokensService:

    @staticmethod
    def execute(data):
        user, errors = UserRegistrationService.register_user(data)

        if not user:
            return None, errors

        tokens = AuthTokenService.generate_tokens_for_user(user)

        response_data = {
            'message': SuccessMessages.REGISTRATION_SUCCESS,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
            },
            'tokens': tokens,
        }

        return response_data, None


class UserAuthenticationService:

    @staticmethod
    def authenticate_user(email, password):

        if not email or not password:
            return None, ErrorMessages.INVALID_CREDENTIALS

        user = authenticate(email=email, password=password)

        if not user:
            return None, ErrorMessages.INVALID_CREDENTIALS

        if not user.is_active:
            return None, ErrorMessages.INACTIVE_ACCOUNT

        return user, None

    @staticmethod
    def update_last_login(user):

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])


class LoginWithTokensService:


    @staticmethod
    def execute(data):

        serializer = UserLoginSerializer(data=data)

        if not serializer.is_valid():
            return None, serializer.errors

        validated_data = serializer.validated_data

        user, auth_error = UserAuthenticationService.authenticate_user(
            validated_data['email'],
            validated_data['password']
        )

        if not user:
            return None, {"non_field_errors": [auth_error]}

        UserAuthenticationService.update_last_login(user)

        tokens = AuthTokenService.generate_tokens_for_user(user)

        response_data = {
            'message': SuccessMessages.LOGIN_SUCCESS,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'last_login': user.last_login,
            },
            'tokens': tokens,
        }

        return response_data, None


class TokenBlacklistService:

    @staticmethod
    def blacklist_refresh_token(refresh_token_str):

        try:
            token = RefreshToken(refresh_token_str)
            token.blacklist()
            return True, None
        except Exception as e:
            return False, str(e)


class LogoutService:


    @staticmethod
    def execute(data):

        serializer = LogoutSerializer(data=data)

        if not serializer.is_valid():
            return None, serializer.errors

        validated_data = serializer.validated_data
        refresh_token = validated_data['refresh_token']

        success, error = TokenBlacklistService.blacklist_refresh_token(refresh_token)

        if success:
            return {"message": SuccessMessages.LOGOUT_SUCCESS}, None

        return None, {"refresh_token": [f"Invalid token: {error}"]}
