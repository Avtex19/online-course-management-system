from rest_framework import serializers

from common.enums import ErrorMessages, TokenFields, UserFields, ValidationFields


class LogoutSerializer(serializers.Serializer):

    refresh_token = serializers.CharField()
    access_token = serializers.CharField(required=False, allow_blank=True)

    def validate_refresh_token(self, value):

        if not value:
            raise serializers.ValidationError(ErrorMessages.REFRESH_TOKEN_REQUIRED)
        return value


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get(UserFields.EMAIL.value)
        password = attrs.get(UserFields.PASSWORD.value)

        if not email or not password:
            raise serializers.ValidationError({
                ValidationFields.NON_FIELD_ERRORS.value: ErrorMessages.INVALID_CREDENTIALS
            })

        return attrs


