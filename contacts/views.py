from rest_framework import generics
from contacts.models import Contacts
from contacts.serializers import UpdateContactSerializer


class ContactUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования контактных данных объектов поставщиков
    """

    serializer_class = UpdateContactSerializer
    queryset = Contacts.objects.all()
