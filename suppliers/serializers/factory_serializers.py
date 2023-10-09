from rest_framework import serializers
from contacts.serializers import ContactSerializer
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

        # Установить contact_owner из factory_data в контактах
        contacts_data['contact_owner'] = factory_data['title']

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
    products_info = ProductSerializer(source='factory_product', many=True, read_only=True)

    class Meta:
        model = Factory
        fields = '__all__'


class FactoryUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Factory
        fields = ('title',)
