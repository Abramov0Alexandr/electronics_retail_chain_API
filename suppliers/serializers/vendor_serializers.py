from rest_framework import serializers
from contacts.serializers import ContactSerializer
from suppliers.models import Vendors


class VendorSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(required=True,)

    class Meta:
        model = Vendors
        fields = '__all__'

    def create(self, validated_data):

        # Извлечь данные для создания объекта RetailChains
        vendor_data = validated_data.copy()
        contacts_data = vendor_data.pop('contacts')

        # Установить contact_owner в модели Contacts данными из vendor_data
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
            # Обработать случай, если данные для модели Contacts недействительны
            raise serializers.ValidationError("Контактные данные не валидны")
