from django.contrib.auth.models import AbstractUser
from django.db import models

from common.enums import UserRole
from .managers import UserManager


class User(AbstractUser):
    """
    Custom User model using email as the primary identifier.
    
    Follows SRP by focusing only on data representation.
    User creation logic is handled by UserManager.
    """
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices(),
        blank=False,
        null=False,
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

