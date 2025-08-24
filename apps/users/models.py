from django.contrib.auth.models import AbstractUser
from django.db import models

from common.enums import UserRole, UserFields
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
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

