from django.contrib.auth.models import AbstractUser
from django.db import models

from common.enums import UserRole


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices(),
        default=UserRole.STUDENT.value,
    )

