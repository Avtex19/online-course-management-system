from datetime import datetime, timezone as dt_timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


User = get_user_model()


class TokenBlacklistService:

	@staticmethod
	def blacklist_refresh_token(refresh_token_str):

		try:
			token = RefreshToken(refresh_token_str)
			token.blacklist()
			return True, None
		except Exception as e:
			return False, str(e)


class AccessTokenBlacklistService:

	@staticmethod
	def blacklist(access_token_str):

		try:
			access_token = AccessToken(access_token_str)
			jti = access_token['jti']

			# Try to find existing OutstandingToken, create if missing
			try:
				outstanding = OutstandingToken.objects.get(jti=jti)
			except OutstandingToken.DoesNotExist:
				user = None
				if access_token.get('user_id'):
					try:
						user = User.objects.get(id=access_token['user_id'])
					except User.DoesNotExist:
						user = None
				created_at_aware = datetime.fromtimestamp(access_token['iat'], tz=dt_timezone.utc)
				expires_at_aware = datetime.fromtimestamp(access_token['exp'], tz=dt_timezone.utc)

				outstanding = OutstandingToken.objects.create(
					token=str(access_token_str),
					jti=jti,
					created_at=created_at_aware,
					expires_at=expires_at_aware,
					user=user,
				)

			BlacklistedToken.objects.get_or_create(token=outstanding)
			return True, None
		except Exception as e:
			return False, str(e)


