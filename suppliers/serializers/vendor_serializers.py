from rest_framework import serializers, status
from contacts.serializers import CreateContactSerializer
from suppliers.models import Vendors, RetailChains, Factory
from suppliers.validators import RequiredSupplierField, NewTitleValidationError


class VendorSelfSupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели Vendors.
    Сериализатор вызывается при создании объекта без указания поставщика.
    Одновременно с созданием объекта Vendors, также создаются связанные с объектом контакты.
    """

    contacts = CreateContactSerializer(required=True)

    class Meta:
        model = Vendors
        fields = '__all__'
        validators = [RequiredSupplierField(),
                      NewTitleValidationError(field='title')]

    def create(self, validated_data):

        # Извлечь данные для создания объекта RetailChains и связанных с ним контактов
        vendor_data = validated_data.copy()
        contacts_data = vendor_data.pop('contacts')

        # Заполнить поле "contact_owner" и "type_owner_organization" в связанных контактах
        contacts_data['contact_owner'] = vendor_data['title']
        contacts_data['type_owner_organization'] = 'Индивидуальный предприниматель'

        contacts = CreateContactSerializer(data=contacts_data)

        if contacts.is_valid():
            # Создать объект Contacts
            contacts_instance = contacts.save()

            # Создать объект Vendors с заполнением поля contacts
            vendor = Vendors.objects.create(contacts=contacts_instance, **vendor_data)
            return vendor


class VendorRelatedSupplierSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели Vendors с указанием поставщика.
    Одновременно с созданием объекта Vendors, также создаются связанные с объектом контакты.
    """

    contacts = CreateContactSerializer(required=True)

    class Meta:
        model = Vendors
        fields = '__all__'
        validators = [NewTitleValidationError(field='title')]

    def create(self, validated_data):

        # Извлечь данные для создания объекта Vendors и связанных с ним контактов
        vendor_data = validated_data.copy()
        vendor_contacts_data = vendor_data.pop('contacts')

        # Извлечь данные для дальнейшего определения поставщика
        supplier_content_type_choice = validated_data.get('supplier_content_type')
        supplier_id = validated_data.get('supplier_id')

        # Проверить, что content_type соответствует определенным моделям
        if supplier_content_type_choice.id in [10, 11]:

            # Определить какая модель будет установлена в качестве поставщика
            supplier_model = RetailChains if supplier_content_type_choice.id == 10 else Factory

            # Проверить, что объект выбранной модели поставщика уже существует, если нет, вызвать исключение
            supplier_instance = supplier_model.objects.filter(id=supplier_id)

            if supplier_instance.exists():

                # Заполнить поле "contact_owner" и "type_owner_organization" в связанных контактах
                vendor_contacts_data['contact_owner'] = vendor_data['title']
                vendor_contacts_data['type_owner_organization'] = 'Индивидуальный предприниматель'
                contacts_serializer = CreateContactSerializer(data=vendor_contacts_data)

                if contacts_serializer.is_valid():
                    # Создать объект Contacts
                    contacts_instance = contacts_serializer.save()

                    # Создать объект Vendors с указанием контактов и поставщика
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
                           'Укажите: supplier_content_type:10 (Розничная сеть), '
                           'supplier_content_type:11 (Завод)',
                           'status': f'{status.HTTP_400_BAD_REQUEST}'})


class VendorsListSerializer(serializers.ModelSerializer):
    """
    Контроллер для получения списка объектов модели Vendors.
    Информация содержит данные поставщика и его контакты.
    """

    vendor_contacts = CreateContactSerializer(source='contacts', read_only=True)
    vendor_title = serializers.CharField(source='title', read_only=True)
    supplier_type = serializers.CharField(source='supplier_content_type', read_only=True)

    class Meta:
        model = Vendors
        exclude = ('contacts', 'title', 'supplier_content_type',)


class VendorUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования поля "title" у объекта модели Vendors.
    При изменении поля "title" также изменяется поле contact_owner в связанных с объектом контактах.
    """

    def update(self, instance, validated_data):

        # Обновить поле "title" у объекта Vendors
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        # Обновить связанные с объектом контакты
        contact_instance = instance.contacts
        contact_instance.contact_owner = validated_data.get('title', contact_instance.contact_owner)
        contact_instance.save()

        return instance

    class Meta:
        model = Vendors
        validators = [NewTitleValidationError(field='title')]
        fields = ('title',)
