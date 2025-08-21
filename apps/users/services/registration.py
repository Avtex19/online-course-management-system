from django.contrib.auth import get_user_model
from common.enums import SuccessMessages

from apps.users.serializers import UserRegistrationSerializer
from apps.users.services.authentication import AuthTokenService


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


