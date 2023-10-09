from django.db import models
from contacts.models import Contacts
from products.models import Products

NULLABLE = {'blank': True, 'null': True}


class Factory(models.Model):

    title = models.CharField(max_length=150, unique=True, verbose_name='Название')

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE,
                                    related_name='factory_contact', verbose_name='Контакты', **NULLABLE)

    manufactured_products = models.ForeignKey(Products, on_delete=models.CASCADE,
                                              related_name='factory_product', verbose_name='Товары', **NULLABLE)

    objects = models.Manager

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk', 'registration_date')
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'

