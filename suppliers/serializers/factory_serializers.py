from rest_framework import serializers
from contacts.serializers import CreateContactSerializer
from products.serializers import ProductSerializer
from suppliers.models import Factory
from suppliers.validators import NewTitleValidationError


class FactoryCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели Factory.
    Одновременно с созданием объекта Factory, также создаются связанные с данным контакты.
    """

    contacts = CreateContactSerializer(required=True)

    class Meta:
        model = Factory
        fields = '__all__'
        validators = [NewTitleValidationError(field='title')]

    def create(self, validated_data):
        # Извлечь данные для создания объекта Factory и связанных с ним контактов
        factory_data = validated_data.copy()
        contacts_data = factory_data.pop('contacts')

        # Заполнить поле "contact_owner" и "type_owner_organization" в связанных контактах
        contacts_data['contact_owner'] = factory_data['title']
        contacts_data['type_owner_organization'] = 'Завод'

        contacts = CreateContactSerializer(data=contacts_data)

        if contacts.is_valid():

            # Создать объект Contacts
            contacts_instance = contacts.save()

            # Создать объект Factory с заполнением поля contacts
            factory = Factory.objects.create(contacts=contacts_instance, **factory_data)
            return factory
        else:
            # Обработать случай, если данные для модели Contacts недействительны
            raise serializers.ValidationError("Invalid data for Contacts")


class FactoryDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения детальной информации об объекте модели Factory.
    Информация содержит данные поставщика, его контакты и продукты.
    """

    factory_contacts = CreateContactSerializer(source='contacts', read_only=True)
    products_info = ProductSerializer(source='factory_product', many=True, read_only=True)
    factory_title = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Factory
        exclude = ('title', 'contacts')


class FactoryUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования поля "title" у объекта модели Factory.
    При изменении поля "title" также изменяется поле contact_owner в связанных с объектом контактах.
    """

    class Meta:
        model = Factory
        validators = [NewTitleValidationError(field='title')]
        fields = ('title',)

    def update(self, instance, validated_data):

        # Обновить поле "title" у объекта Factory
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Обновить связанные с объектом контакты
        contact_instance = instance.contacts
        contact_instance.contact_owner = validated_data.get('title', contact_instance.contact_owner)
        contact_instance.save()

        return instance
