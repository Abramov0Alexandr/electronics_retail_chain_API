from django.db import models
from django.contrib.auth import get_user_model
from contacts.models import Contacts
from products.models import Products


class RetailNetwork(models.Model):

    SUPPLIER_CHOICES = [
        ('Factory', 'Завод'),
        ('Vendor', 'Индивидуальный предприниматель'),
    ]

    title = models.CharField(max_length=150, unique=True, verbose_name='Розничная сеть')

    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE,
                                    related_name='retail_contacts', verbose_name='Контакты')

    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукты')

    # supplier = models.ForeignKey(, on_delete=models.PROTECT)

    debt_amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Долг перед поставщиком')

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 related_name='retail_employee', verbose_name='Работник')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk', 'registration_date')
        verbose_name = 'Розничная сеть'
        verbose_name_plural = 'Розничные сети'
