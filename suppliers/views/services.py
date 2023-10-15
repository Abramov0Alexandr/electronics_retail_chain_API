from suppliers.models import RetailChains, Vendors


def update_vendor_supplier_title(sender, instance, **kwargs):
    """
    Общая функция для обновления полей объектов модели Vendors.
    """

    vendors = Vendors.objects.filter(supplier_id=instance.id)

    if vendors.exists():  # Проверить наличие совпадающих объектов
        vendor = vendors.first()  # Получить первый объект из QuerySet
        vendor.supplier_title = instance.title
        vendor.save()


def update_retail_chain_supplier_title(sender, instance, **kwargs):
    """
    Общая функция для обновления полей объектов модели RetailChains.
    """

    retail_chains = RetailChains.objects.filter(supplier_id=instance.id)

    if retail_chains.exists():  # Проверить наличие совпадающих объектов
        retail_chain = retail_chains.first()  # Получить первый объект из QuerySet
        retail_chain.supplier_title = instance.title
        retail_chain.save()
