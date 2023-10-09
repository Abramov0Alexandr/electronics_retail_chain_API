from rest_framework import serializers
from contacts.serializers import ContactSerializer
from employees.serializers import EmployeeSerializer
from products.serializers import ProductSerializer
from suppliers.models import Factory


class MainFactorySerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(required=True)

    class Meta:
        model = Factory
        fields = '__all__'

    def create(self, validated_data):
        # Извлечь данные для создания объекта Factory
        factory_data = validated_data.copy()
        contacts_data = factory_data.pop('contacts')

        contacts = ContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Сохранить Контакты
            contacts_instance = contacts.save()

            # Создать объект Factory с указанием Контактов и Продуктов
            factory = Factory.objects.create(contacts=contacts_instance, **factory_data)
            return factory
        else:
            # Обработать случай, если данные для Контактов или Продуктов недействительны
            raise serializers.ValidationError("Invalid data for Contacts")


class FactoryDetailSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(read_only=True)
    manufactured_products = ProductSerializer(read_only=True)
    employees = EmployeeSerializer(read_only=True)

    class Meta:
        model = Factory
        fields = '__all__'
