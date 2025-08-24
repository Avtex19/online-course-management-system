from rest_framework import serializers

from common.enums import ErrorMessages, UserRole, UserFields
from apps.users.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150, )
    role = serializers.ChoiceField(choices=UserRole.choices(), required=True)

    class Meta:
        model = User
        fields = [
            UserFields.EMAIL.value,
            UserFields.FIRST_NAME.value,
            UserFields.LAST_NAME.value,
            UserFields.ROLE.value,
            UserFields.PASSWORD.value,
            UserFields.PASSWORD_CONFIRM.value,
        ]

    def validate(self, attrs):
        password = attrs.get(UserFields.PASSWORD.value)
        password_confirm = attrs.get(UserFields.PASSWORD_CONFIRM.value)
        if password != password_confirm:
            raise serializers.ValidationError({
                UserFields.PASSWORD_CONFIRM.value: ErrorMessages.PASSWORDS_DO_NOT_MATCH
            })
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            UserFields.ID.value,
            UserFields.EMAIL.value,
            UserFields.FIRST_NAME.value,
            UserFields.LAST_NAME.value,
            UserFields.ROLE.value,
        ]
        read_only_fields = [UserFields.ID.value]
