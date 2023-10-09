from rest_framework import generics
from contacts.models import Contacts
from contacts.serializers import ContactSerializer


class ContactUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ContactSerializer
    queryset = Contacts.objects.all()
