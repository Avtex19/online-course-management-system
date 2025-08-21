from django.contrib.auth.base_user import BaseUserManager

from common.enums import ErrorMessages, UserFields


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError(ErrorMessages.EMAIL_REQUIRED)
        
        email = self.normalize_email(email)
        user = self.model(**{UserFields.EMAIL: email}, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault(UserFields.IS_STAFF, True)
        extra_fields.setdefault(UserFields.IS_SUPERUSER, True)
        extra_fields.setdefault(UserFields.IS_ACTIVE, True)

        if extra_fields.get(UserFields.IS_STAFF) is not True:
            raise ValueError(ErrorMessages.SUPERUSER_STAFF_REQUIRED)
        if extra_fields.get(UserFields.IS_SUPERUSER) is not True:
            raise ValueError(ErrorMessages.SUPERUSER_PERMISSION_REQUIRED)

        return self.create_user(email, password, **extra_fields)
