from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_manager import CustomUserManager


NULLABLE = {'blank': True, 'null': True}


class Employee(AbstractUser):
    """
    Расширение стандартной модели пользователя в соответствии с требованиями текущего проекта.
    """

    # EMPLOYER_CHOICES = [
    #     ('Factory', 'Завод'),
    #     ('RetailNetwork', 'Розничная сеть'),
    #     ('Vendor', 'Индивидуальный предприниматель'),
    # ]

    username = None

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Email')

    # В дальнейшем, при регистрации пользователя через эндпоинт поставщика заполнять это поле
    # employer = models.CharField(max_length=13, choices=EMPLOYER_CHOICES, null=True,
    #                             default=None, verbose_name='Организация')

    employer_title = models.CharField(max_length=150, verbose_name='Организация', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='Статус активности')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.employer_title}'

    class Meta:
        ordering = ('pk', 'employer_title',)
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
