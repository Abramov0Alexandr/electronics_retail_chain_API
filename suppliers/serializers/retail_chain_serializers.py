from rest_framework import serializers
from contacts.serializers import ContactSerializer
from suppliers.models import RetailChains, Factory
from suppliers.serializers import FactoryDetailSerializer


class MainRetailChainsSerializer(serializers.ModelSerializer):

    supplier = serializers.PrimaryKeyRelatedField(queryset=Factory.objects.all(), required=True, read_only=False)

    contacts = ContactSerializer(required=True, read_only=False)

    class Meta:
        model = RetailChains
        fields = ('id', 'title', 'contacts', 'supplier',)

    def create(self, validated_data):
        # Извлечь данные для создания объекта RetailChains
        retail_chain_data = validated_data.copy()
        contacts_data = retail_chain_data.pop('contacts')

        # Установить contact_owner в модели Contacts данными из retail_chain_data(:validated_data)
        contacts_data['contact_owner'] = retail_chain_data['title']

        contacts = ContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Сохранить экземпляр объекта Contacts
            contacts_instance = contacts.save()

            # Создать объект RetailChains с заполнением поля contacts
            retail_chain = RetailChains.objects.create(contacts=contacts_instance, **retail_chain_data)
            return retail_chain
        else:
            # Обработать случай, если данные для модели Contacts недействительны
            raise serializers.ValidationError("Контактные данные не валидны")


class RetailChainListSerializer(serializers.ModelSerializer):

    supplier = FactoryDetailSerializer(read_only=True)
    retail_chain_contacts = ContactSerializer(source='contacts', read_only=True)
    retail_chain_title = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = RetailChains
        exclude = ('title', 'contacts')


class RetailChainUpdateSerializer(serializers.ModelSerializer):
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
        model = RetailChains
        fields = ('title',)

