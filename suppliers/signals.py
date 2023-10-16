from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from suppliers.models import RetailChains, Vendors, Factory
from suppliers.views import services


@receiver(post_save, sender=RetailChains)
def update_vendor_supplier_retail_chain_title(sender, instance, **kwargs):
    """
    Сигнал для обновления поля supplier_title (наименование поставщика) модели Vendors.
    При изменении названия розничной сети, новое название также изменяется и у связанного объекта заказчика.
    Данное поле носит только информационный характер.
    """

    services.update_vendor_supplier_title(sender, instance, **kwargs)


@receiver(post_save, sender=Factory)
def update_vendor_supplier_factory_title(sender, instance, **kwargs):
    """
    Сигнал для обновления поля supplier_title (наименование поставщика) модели Vendors.
    При изменении названия завода, новое название также изменяется и у связанного объекта заказчика.
    Данное поле носит только информационный характер.
    """

    services.update_vendor_supplier_title(sender, instance, **kwargs)


@receiver(post_save, sender=Factory)
def update_retail_chain_supplier_factory_title(sender, instance, **kwargs):
    """
    Сигнал для обновления поля supplier_title (наименование поставщика) модели RetailChains.
    При изменении названия завода, новое название также изменяется и у связанного объекта заказчика.
    Данное поле носит только информационный характер.
    """

    services.update_retail_chain_supplier_title(sender, instance, **kwargs)


@receiver(post_save, sender=Vendors)
def update_retail_chain_supplier_vendor_title(sender, instance, **kwargs):
    """
    Сигнал для обновления поля supplier_title (наименование поставщика) модели RetailChains.
    При изменении названия розничной сети, новое название также изменяется и у связанного объекта заказчика.
    Данное поле носит только информационный характер.
    """

    services.update_retail_chain_supplier_title(sender, instance, **kwargs)


@receiver(post_delete, sender=Vendors)
def update_retail_chain_fields(sender, instance, **kwargs):
    """
    Сигнал используется для обновления полей supplier_title, supplier_content_type, supplier_id (устанавливается None)
    при удалении связанного объекта поставщика (Vendors).
    """

    # Получить все объекты RetailChains, которые связаны с удаляемым Vendors
    retail_chain = RetailChains.objects.filter(supplier_id=instance.id)

    # Обновить поля в найденных объектах Vendors
    retail_chain.update(
        supplier_title=None,
        supplier_content_type=None,
        supplier_id=None
    )


@receiver(post_delete, sender=RetailChains)
def update_vendor_fields(sender, instance, **kwargs):
    """
    Сигнал используется для обновления полей supplier_title, supplier_content_type, supplier_id (устанавливается None)
    при удалении связанного объекта поставщика (RetailChains).
    """

    # Получить все объекты Vendors, которые связаны с удаляемым RetailChains
    vendors = Vendors.objects.filter(supplier_id=instance.id)

    # Обновить поля в найденных объектах Vendors
    vendors.update(
        supplier_title=None,
        supplier_content_type=None,
        supplier_id=None
    )
