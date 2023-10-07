from django.contrib.auth import get_user_model
from django.db import models
from contacts.models import Contacts
from products.models import Products


class Vendors(models.Model):

    SUPPLIER_CHOICES = [
        ('Factory', 'Завод'),
        ('RetailNetwork', 'Розничная сеть'),
    ]

    title = models.CharField(max_length=150, unique=True, verbose_name='Индивидуальный предприниматель')
    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE,
                                    related_name='vendor_contacts', verbose_name='Контакты')

    products = models.ForeignKey(Products, on_delete=models.CASCADE, verbose_name='Продукты')
    # supplier = models.ForeignKey(, on_delete=models.PROTECT)

    debt_amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name='Долг перед поставщиком')

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    employee = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                 related_name='vendor_employee', verbose_name='Работник')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk', 'registration_date')
        verbose_name = 'Индивидуальный предприниматель'
        verbose_name_plural = 'Индивидуальные предприниматели'
