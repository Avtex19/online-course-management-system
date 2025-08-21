from rest_framework import serializers

from common.enums import ErrorMessages, UserRole
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=UserRole.choices(), required=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "password_confirm",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError({
                "password_confirm": ErrorMessages.PASSWORDS_DO_NOT_MATCH
            })
        return attrs


class LogoutSerializer(serializers.Serializer):

    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):

        if not value:
            raise serializers.ValidationError(ErrorMessages.REFRESH_TOKEN_REQUIRED)
        return value


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
        ]
        read_only_fields = ["id"]


class UserLoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError({
                "non_field_errors": ErrorMessages.INVALID_CREDENTIALS
            })

        return attrs
