from django.db import IntegrityError
from rest_framework import serializers, status

from contacts.models import Contacts
from contacts.serializers import ContactSerializer
from suppliers.models import Vendors, RetailChains, Factory
from suppliers.validators import RequiredSupplierField


class VendorSelfSupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания простого ИП (без указания поставщика)
    """

    contacts = ContactSerializer(required=True)

    class Meta:
        model = Vendors
        fields = '__all__'
        validators = [RequiredSupplierField()]

    def create(self, validated_data):

        # Извлечь все необходимые для дальнейшей работы данные
        vendor_data = validated_data.copy()
        contacts_data = vendor_data.pop('contacts')

        # Установить contact_owner и type_owner_organization в модели Contacts
        contacts_data['contact_owner'] = vendor_data['title']
        contacts_data['type_owner_organization'] = 'Индивидуальный предприниматель'

        contacts = ContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Сохранить экземпляр объекта Contacts
            contacts_instance = contacts.save()

            # Создать объект Vendors с заполнением поля contacts
            vendor = Vendors.objects.create(contacts=contacts_instance, **vendor_data)
            return vendor

        else:
            raise serializers.ValidationError("Контактные данные не валидны")


class VendorRelatedSupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания ИП с указанием поставщика
    """

    contacts = ContactSerializer(required=True)

    class Meta:
        model = Vendors
        fields = '__all__'

    def create(self, validated_data):

        # Извлечь все необходимые для дальнейшей работы данные
        vendor_data = validated_data.copy()
        vendor_contacts_data = vendor_data.pop('contacts')
        supplier_content_type_choice = validated_data.get('supplier_content_type')
        supplier_id = validated_data.get('supplier_id')

        # Проверить, что content_type соответствует определенным моделям
        if supplier_content_type_choice.id in [9, 11]:

            # Определить какая модель будет установлена в качестве поставщика
            supplier_model = Factory if supplier_content_type_choice.id == 9 else RetailChains

            # Проверить, что объекты поставщика уже существуют, если нет, вызвать исключение
            supplier_instance = supplier_model.objects.filter(id=supplier_id)

            if supplier_instance.exists():

                # Установить contact_owner и type_owner_organization в модели Contacts
                vendor_contacts_data['contact_owner'] = vendor_data['title']
                vendor_contacts_data['type_owner_organization'] = 'Индивидуальный предприниматель'
                contacts_serializer = ContactSerializer(data=vendor_contacts_data)

                if contacts_serializer.is_valid():
                    contacts_instance = contacts_serializer.save()

                    # Создание объекта Vendors
                    vendor = Vendors.objects.create(
                        contacts=contacts_instance,
                        supplier_title=supplier_model.objects.get(id=supplier_id).title,
                        **vendor_data)
                    return vendor

            else:
                raise serializers.ValidationError(
                    {'detail': f'{supplier_content_type_choice.name} c ID:{supplier_id} не зарегистрирован',
                     'status': f'status:{status.HTTP_400_BAD_REQUEST}'})

        else:
            raise serializers.ValidationError(
                {'detail': 'Указанный некорректный id типа поставщика. '
                           'Укажите: supplier_content_type:9 (Завод), '
                           'supplier_content_type:11 (Розничная сеть)',
                           'status': f'{status.HTTP_400_BAD_REQUEST}'})


class VendorsListSerializer(serializers.ModelSerializer):
    """Сериализатор для выполнения GET запроса"""
    contacts = ContactSerializer(read_only=True)

    class Meta:
        model = Vendors
        exclude = ('supplier_content_type',)


class VendorUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации об объекте модели Vendors.
    Сериализатор позволяет изменить только название объекта, при этом,
    в связанном контакте модели Contacts аналогично изменяется поле contact_owner
    """

    def update(self, instance, validated_data):
        new_title = validated_data.get('title')
        if new_title and new_title != instance.title:

            # Проверить, существует ли запись с новым title
            if Vendors.objects.filter(title=new_title).exists():
                raise serializers.ValidationError(
                    {'detail': f'Название {new_title} занято.'})

            instance.title = new_title
            instance.save()

        contact_instance = instance.contacts
        contact_owner = validated_data.get('title')

        if contact_owner and contact_owner != contact_instance.contact_owner:
            contact_instance.contact_owner = contact_owner
            contact_instance.save()

        return instance

    class Meta:
        model = Factory
        fields = ('title',)
