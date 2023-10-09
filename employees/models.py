from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_manager import CustomUserManager


NULLABLE = {'blank': True, 'null': True}


class Employee(AbstractUser):
    """
    Расширение стандартной модели пользователя в соответствии с требованиями текущего проекта.
    """

    username = None

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True, verbose_name='Статус активности')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('pk',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
