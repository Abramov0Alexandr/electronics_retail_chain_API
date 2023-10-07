from django.db import models


class Contacts(models.Model):

    email = models.EmailField(max_length=50, unique=True, verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    building_number = models.CharField(max_length=10, verbose_name='Номер дома')

    def __str__(self):
        return f'{self.email} {self.country}'

    class Meta:
        ordering = ('pk', )
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
