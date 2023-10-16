from rest_framework import serializers, status
from contacts.serializers import CreateContactSerializer
from suppliers.models import RetailChains, Factory, Vendors
from suppliers.validators import RequiredSupplierField, NewTitleValidationError


class RetailChainSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели RetailChains.
    Сериализатор вызывается при создании объекта без указания поставщика.
    Одновременно с созданием объекта RetailChains, также создаются связанные с объектом контакты.
    """

    contacts = CreateContactSerializer(required=True)

    class Meta:
        model = RetailChains
        fields = '__all__'
        validators = [RequiredSupplierField(),
                      NewTitleValidationError(field='title')]

    def create(self, validated_data):

        # Извлечь данные для создания объекта RetailChains и связанных с ним контактов
        retail_chain_data = validated_data.copy()
        contacts_data = retail_chain_data.pop('contacts')

        # Заполнить поле "contact_owner" и "type_owner_organization" в связанных контактах
        contacts_data['contact_owner'] = retail_chain_data['title']
        contacts_data['type_owner_organization'] = 'Розничная сеть'

        contacts = CreateContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Создать объект Contacts
            contacts_instance = contacts.save()

            # Создать объект RetailChains с заполнением поля contacts
            retail_chain = RetailChains.objects.create(contacts=contacts_instance, **retail_chain_data)
            return retail_chain


class RetailChainSupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели RetailChains с указанием поставщика.
    Одновременно с созданием объекта RetailChains, также создаются связанные с объектом контакты.
    """

    contacts = CreateContactSerializer(required=True)

    class Meta:
        model = RetailChains
        fields = '__all__'
        validators = [NewTitleValidationError(field='title')]

    def create(self, validated_data):

        # Извлечь данные для создания объекта RetailChains и связанных с ним контактов
        retail_chain_data = validated_data.copy()
        retail_chain_contacts_data = retail_chain_data.pop('contacts')

        # Извлечь данные для дальнейшего определения поставщика
        supplier_content_type_choice = validated_data.get('supplier_content_type')
        supplier_id = validated_data.get('supplier_id')

        # Проверить, что content_type соответствует определенным моделям
        if supplier_content_type_choice.id in [9, 11]:

            # Определить какая модель будет установлена в качестве поставщика
            supplier_model = Vendors if supplier_content_type_choice.id == 9 else Factory

            # Проверить, что объект выбранной модели поставщика уже существует, если нет, вызвать исключение
            supplier_instance = supplier_model.objects.filter(id=supplier_id)

            if supplier_instance.exists():

                # Заполнить поле "contact_owner" и "type_owner_organization" в связанных контактах
                retail_chain_contacts_data['contact_owner'] = retail_chain_data['title']
                retail_chain_contacts_data['type_owner_organization'] = 'Розничная сеть'
                contacts_serializer = CreateContactSerializer(data=retail_chain_contacts_data)

                if contacts_serializer.is_valid():
                    # Создать объект Contacts
                    contacts_instance = contacts_serializer.save()

                    # Создать объект RetailChains с указанием контактов и поставщика
                    retail_chain = RetailChains.objects.create(
                        contacts=contacts_instance,
                        supplier_title=supplier_model.objects.get(id=supplier_id).title,
                        **retail_chain_data)
                    return retail_chain

            else:
                raise serializers.ValidationError(
                    {'detail': f'{supplier_content_type_choice.name} c ID:{supplier_id} не зарегистрирован',
                     'status': f'status:{status.HTTP_400_BAD_REQUEST}'})

        else:
            raise serializers.ValidationError(
                {'detail': 'Указанный некорректный id типа поставщика. '
                           'Укажите: supplier_content_type:9 (Индивидуальный предприниматель), '
                           'supplier_content_type:11 (Завод)',
                 'status': f'{status.HTTP_400_BAD_REQUEST}'})


class RetailChainListSerializer(serializers.ModelSerializer):
    """
    Контроллер для получения списка объектов модели RetailChains.
    Информация содержит данные поставщика и его контакты.
    """

    retail_chain_contacts = CreateContactSerializer(source='contacts', read_only=True)
    retail_chain_title = serializers.CharField(source='title', read_only=True)
    supplier_type = serializers.CharField(source='supplier_content_type', read_only=True)

    class Meta:
        model = RetailChains
        exclude = ('contacts', 'title', 'supplier_content_type',)


class RetailChainUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования поля "title" у объекта модели Factory.
    При изменении поля "title" также изменяется поле contact_owner в связанных с объектом контактах.
    """

    def update(self, instance, validated_data):

        # Обновить поле "title" у объекта RetailChains
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Обновить связанные с объектом контакты
        contact_instance = instance.contacts
        contact_instance.contact_owner = validated_data.get('title', contact_instance.contact_owner)
        contact_instance.save()

        return instance

    class Meta:
        model = RetailChains
        validators = [NewTitleValidationError(field='title')]
        fields = ('title',)
