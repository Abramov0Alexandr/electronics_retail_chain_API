from django.db import models
from contacts.models import Contacts
from products.models import Products
from django.contrib.auth import get_user_model


class Factory(models.Model):

    title = models.CharField(max_length=150, unique=True, verbose_name='Название')

    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE,
                                    related_name='factory_contacts', verbose_name='Контакты')

    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукты')

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 related_name='factory_employee',verbose_name='Сотрудники')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk', 'registration_date')
        verbose_name = 'Завод'
        verbose_name_plural = 'Заводы'
