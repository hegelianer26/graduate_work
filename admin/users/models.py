import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import MyUserManager


class CustomUser(AbstractBaseUser):
    id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    username = models.CharField(verbose_name='username', max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    # строка с именем поля модели, которая используется в качестве уникального идентификатора
    USERNAME_FIELD = 'username'

    # менеджер модели
    objects = MyUserManager()

    def __str__(self):
        return f'{self.username} {self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
