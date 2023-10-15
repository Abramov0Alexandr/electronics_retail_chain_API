from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework import serializers, status
from contacts.models import Contacts
from suppliers.models import RetailChains, Vendors


@receiver(post_save, sender=RetailChains)
def update_related_contact(sender, instance, **kwargs):
    """
    Сигнал для обновления поля contact_owner модели Contacts.
    При изменении названия розничной сети, новое название также изменяется и в связанных контактах.

    Изначально, происходит проверка на то, что работа по обновлению контакта будет вестись у уже существующего
    объекта. В случае, если же происходит первоначальное создание объекта, то он исключается из работы сигнала.
    """

    # Исключить вновь созданный объект из работы и проверить, что новое название не занято другими объектами
    if Contacts.objects.exclude(id=instance.contacts_id).filter(contact_owner=instance.title).exists():

        # Инициировать ошибку, если в поле contact_owner уже указано такое же значение
        raise serializers.ValidationError(
            {'detail': f'Название {instance.title} уже используется',
             'status': f'{status.HTTP_400_BAD_REQUEST}'})

    else:
        related_contacts = Contacts.objects.get(id=instance.contacts_id)
        related_contacts.contact_owner = instance.title
        related_contacts.save()


@receiver(post_save, sender=RetailChains)
def update_vendor_supplier_title(sender, instance, **kwargs):
    """
    Сигнал для обновления поля supplier_title (наименование поставщика) модели Vendors.
    При изменении названия розничной сети, новое название также изменяется и у связанного объекта заказчика.
    Данное поле носит только информационный характер.
    """

    vendors = Vendors.objects.filter(supplier_id=instance.id)

    if vendors.exists():  # Проверить наличие совпадающих объектов
        vendor = vendors.first()  # Получить первый объект из QuerySet
        vendor.supplier_title = instance.title
        vendor.save()


@receiver(post_save, sender=Vendors)
def update_retail_chain_supplier_title(sender, instance, **kwargs):
    """
    Сигнал для обновления поля supplier_title (наименование поставщика) модели RetailChains.
    При изменении названия розничной сети, новое название также изменяется и у связанного объекта заказчика.
    Данное поле носит только информационный характер.
    """

    retail_chains = RetailChains.objects.filter(supplier_id=instance.id)

    if retail_chains.exists():  # Проверить наличие совпадающих объектов
        retail_chain = retail_chains.first()  # Получить первый объект из QuerySet
        retail_chain.supplier_title = instance.title
        retail_chain.save()


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
