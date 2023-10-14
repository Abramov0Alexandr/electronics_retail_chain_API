from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from contacts.models import Contacts


NULLABLE = {'blank': True, 'null': True}


class Vendors(models.Model):

    title = models.CharField(max_length=150, unique=True, verbose_name='Название')

    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE,
                                    related_name='vendor_contacts', verbose_name='Контакты')

    supplier_title = models.CharField(max_length=250, verbose_name='Наименование поставщика', **NULLABLE)
    supplier_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, **NULLABLE,)
    supplier_id = models.CharField(max_length=250, verbose_name='ID поставщика', **NULLABLE)
    supplier = GenericForeignKey('supplier_content_type', 'supplier_id',)

    debt_amount = models.DecimalField(max_digits=11, decimal_places=2,
                                      default=0, verbose_name='Задолженность перед поставщиком')
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk', 'registration_date')
        verbose_name = 'Индивидуальный предприниматель'
        verbose_name_plural = 'Индивидуальные предприниматели'
