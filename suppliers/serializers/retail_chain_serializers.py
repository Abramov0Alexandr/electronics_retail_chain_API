from rest_framework import serializers, status
from contacts.serializers import ContactSerializer
from suppliers.models import RetailChains, Factory, Vendors
from suppliers.serializers import FactoryDetailSerializer
from suppliers.validators import RequiredSupplierField, NewTitleValidationError


class RetailChainSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(required=True)

    class Meta:
        model = RetailChains
        fields = '__all__'
        validators = [RequiredSupplierField()]

    def create(self, validated_data):

        # Извлечь данные для создания объекта RetailChains
        retail_chain_data = validated_data.copy()
        contacts_data = retail_chain_data.pop('contacts')

        # Установить contact_owner и type_owner_organization в модели Contacts
        contacts_data['contact_owner'] = retail_chain_data['title']
        contacts_data['type_owner_organization'] = 'Розничная сеть'

        contacts = ContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Сохранить экземпляр объекта Contacts
            contacts_instance = contacts.save()

            # Создать объект RetailChains с заполнением поля contacts
            retail_chain = RetailChains.objects.create(contacts=contacts_instance, **retail_chain_data)
            return retail_chain

        else:
            raise serializers.ValidationError({'detail': f'Название \'{retail_chain_data["title"]}\' уже используется',
                                               'status': f'{status.HTTP_400_BAD_REQUEST}'})


class RetailChainSupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания ИП с указанием поставщика
    """

    contacts = ContactSerializer(required=True)

    class Meta:
        model = RetailChains
        fields = '__all__'

    def create(self, validated_data):

        # Извлечь все необходимые для дальнейшей работы данные
        vendor_data = validated_data.copy()
        vendor_contacts_data = vendor_data.pop('contacts')
        supplier_content_type_choice = validated_data.get('supplier_content_type')
        supplier_id = validated_data.get('supplier_id')

        # Проверить, что content_type соответствует определенным моделям
        if supplier_content_type_choice.id in [9, 10]:

            # Определить какая модель будет установлена в качестве поставщика
            supplier_model = Factory if supplier_content_type_choice.id == 9 else Vendors

            # Проверить, что объекты поставщика уже существуют, если нет, вызвать исключение
            supplier_instance = supplier_model.objects.filter(id=supplier_id)

            if supplier_instance.exists():

                # Установить contact_owner и type_owner_organization в модели Contacts
                vendor_contacts_data['contact_owner'] = vendor_data['title']
                vendor_contacts_data['type_owner_organization'] = 'Розничная сеть'
                contacts_serializer = ContactSerializer(data=vendor_contacts_data)

                if contacts_serializer.is_valid():
                    contacts_instance = contacts_serializer.save()

                    # Создание объекта Vendors
                    vendor = RetailChains.objects.create(
                        contacts=contacts_instance,
                        supplier_title=supplier_model.objects.get(id=supplier_id).title,
                        **vendor_data)
                    return vendor

                else:
                    raise serializers.ValidationError(
                        {'detail': f'{contacts_serializer.errors.get("contact_owner")[0]}',
                         'status': f'{status.HTTP_400_BAD_REQUEST}'})
            else:
                raise serializers.ValidationError(
                    {'detail': f'{supplier_content_type_choice.name} c ID:{supplier_id} не зарегистрирован',
                     'status': f'status:{status.HTTP_400_BAD_REQUEST}'})

        else:
            raise serializers.ValidationError(
                {'detail': 'Указанный некорректный id типа поставщика. '
                           'Укажите: supplier_content_type:9 (Завод), '
                           'supplier_content_type:10 (Индивидуальный предприниматель)',
                 'status': f'{status.HTTP_400_BAD_REQUEST}'})


class RetailChainListSerializer(serializers.ModelSerializer):

    supplier = FactoryDetailSerializer(read_only=True)
    retail_chain_contacts = ContactSerializer(source='contacts', read_only=True)
    retail_chain_title = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = RetailChains
        exclude = ('title', 'contacts')


class RetailChainUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации об объекте модели RetailChains.
    Сериализатор вместе с названием объекта, обновляет поле contact_owner модели Contacts
    """

    class Meta:
        model = RetailChains
        validators = [NewTitleValidationError(field='title')]
        fields = ('title',)

