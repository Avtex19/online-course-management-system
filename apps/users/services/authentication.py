from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import UserLoginSerializer

User = get_user_model()


class AuthTokenService:

    @staticmethod
    def generate_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserAuthenticationService:

    @staticmethod
    def authenticate_user(email, password):

        if not email or not password:
            return None, "Invalid email or password"

        user = authenticate(email=email, password=password)

        if not user:
            return None, "Invalid email or password"

        if not user.is_active:
            return None, "Account is disabled"

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
            'message': "Login successful",
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
