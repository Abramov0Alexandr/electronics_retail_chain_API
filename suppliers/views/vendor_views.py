from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import Vendors
from suppliers.serializers import (VendorSelfSupplierSerializer, VendorRelatedSupplierSerializer,
                                   VendorsListSerializer, VendorUpdateSerializer)


class VendorCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания объекта Vendors.
    """

    def get_serializer_class(self):
        """
        В зависимости от переданных в POST запросе данных, происходит выбор сериализатора.
        """

        supplier_content_type_choice = self.request.data.get('supplier_content_type')
        supplier_id = self.request.data.get('supplier_id')

        if supplier_content_type_choice and supplier_id:
            return VendorRelatedSupplierSerializer

        else:
            return VendorSelfSupplierSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorsListAPIView(generics.ListAPIView):
    """
    Контроллер для просмотра списка зарегистрированных ИП.
    """
    queryset = Vendors.objects.all()
    serializer_class = VendorsListSerializer


class VendorUpdateAPIView(generics.UpdateAPIView):
    queryset = Vendors.objects.all()
    serializer_class = VendorUpdateSerializer


class VendorDeleteAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели Vendors и связанный с ним контакт.
    """

    queryset = Vendors.objects.all()

    def delete(self, request, *args, **kwargs):

        vendor = self.get_object()
        contacts = vendor.contacts

        if contacts:
            contacts.delete()

        self.perform_destroy(vendor)  # Вызвать стандартный метод удаления для розничной сети

        # Возвращаем успешный ответ
        return Response(
            {'detail': f'Индивидуальный предприниматель \'{vendor.title}\' '
                       f'и связанные с ним контакты были успешно удалены'},
            status=status.HTTP_204_NO_CONTENT)
