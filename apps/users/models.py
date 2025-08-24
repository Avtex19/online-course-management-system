from django.contrib.auth.models import AbstractUser
from django.db import models

from common.enums import UserRole, UserFields, ModelVerboseNames
from .managers import UserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices(),
        blank=False,
        null=False,
    )
    
    USERNAME_FIELD = UserFields.EMAIL.value
    REQUIRED_FIELDS = [UserFields.FIRST_NAME.value, UserFields.LAST_NAME.value, UserFields.ROLE.value]
    
    objects = UserManager()
    
    def __str__(self):
        return getattr(self, UserFields.EMAIL.value)
    
    class Meta:
        verbose_name = ModelVerboseNames.USER.value
        verbose_name_plural = ModelVerboseNames.USERS.value

