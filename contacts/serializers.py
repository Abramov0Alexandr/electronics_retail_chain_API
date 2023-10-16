from rest_framework import serializers
from .models import Contacts


class CreateContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор используется при создании контактов для объектов поставщиков.
    """

    class Meta:
        model = Contacts
        fields = '__all__'


class UpdateContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор используется при редактировании контактов объектов поставщиков.
    """

    class Meta:
        model = Contacts
        exclude = ('type_owner_organization',)
