import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = ((USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin'))
    role = models.CharField(
        'Роль', max_length=100, choices=ROLE_CHOICES, default=USER
    )
    bio = models.TextField('Биография', blank=True, null=True)
    confirmation_code = models.CharField(
        max_length=70, unique=True, blank=True, null=True, default=uuid.uuid4
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_admin
