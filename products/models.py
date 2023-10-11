from django.db import models
from suppliers.models import Factory


NULLABLE = {'blank': True, 'null': True}


class Products(models.Model):
    title = models.CharField(max_length=250, verbose_name='Продукт')
    model = models.CharField(max_length=250, verbose_name='Модель', **NULLABLE)
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата выпуска на рынок')

    manufacturer = models.ForeignKey(Factory, on_delete=models.CASCADE,
                                     related_name='factory_product', verbose_name='Производитель')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('pk', 'title',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
