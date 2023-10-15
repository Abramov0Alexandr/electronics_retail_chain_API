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

        # Установить contact_owner в модели Contacts данными из retail_chain_data
        contacts_data['contact_owner'] = factory_data['title']
        contacts_data['type_owner_organization'] = 'Завод'

        contacts = ContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Сохранить экземпляр объекта Contacts
            contacts_instance = contacts.save()

            # Создать объект Factory с заполнением поля contacts
            factory = Factory.objects.create(contacts=contacts_instance, **factory_data)
            return factory
        else:
            # Обработать случай, если данные для модели Contacts недействительны
            raise serializers.ValidationError("Invalid data for Contacts")


class FactoryDetailSerializer(serializers.ModelSerializer):

    factory_contacts = ContactSerializer(source='contacts', read_only=True)
    products_info = ProductSerializer(source='factory_product', many=True, read_only=True)
    factory_title = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Factory
        exclude = ('title', 'contacts')


class FactoryUpdateSerializer(serializers.ModelSerializer):
    """
    При изменении названия завода ток же изменяется и поле contact_owner в модели Контакты
    """

    def update(self, instance, validated_data):

        # Обновляем название завода
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Обновляем контакты
        contact_instance = instance.contacts
        contact_instance.contact_owner = validated_data.get('title', contact_instance.contact_owner)
        contact_instance.save()

        return instance

    class Meta:
        model = Factory
        fields = ('title',)
