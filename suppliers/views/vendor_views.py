from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import Vendors
from suppliers import serializers


class VendorCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания нового объекта модели Vendors.
    """

    def get_serializer_class(self):
        """
        Метод для определения будет ли создаваться объект без поставщика или с поставщиком.
        :return: Сериализатор для создания объекта модели Vendors.
        """

        supplier_content_type_choice = self.request.data.get('supplier_content_type')
        supplier_id = self.request.data.get('supplier_id')

        if supplier_content_type_choice and supplier_id:
            return serializers.VendorRelatedSupplierSerializer

        else:
            return serializers.VendorSelfSupplierSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorsListAPIView(generics.ListAPIView):
    """
    Контроллер для получения списка объектов модели Vendors.
    """

    queryset = Vendors.objects.all()
    serializer_class = serializers.VendorsListSerializer


class VendorUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования объекта модели Vendors.
    """

    queryset = Vendors.objects.all()
    serializer_class = serializers.VendorUpdateSerializer


class VendorDeleteAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели Vendors.
    Контроллер одновременно с удалением объект поставщика, удаляет и связанные с ним контакты.
    """

    queryset = Vendors.objects.all()

    def delete(self, request, *args, **kwargs):

        vendor = self.get_object()  # Получить объект поставщика
        contacts = vendor.contacts  # Получить связанные с объектом контакты

        if contacts:  # Удалить связанные контакты
            contacts.delete()

        self.perform_destroy(vendor)  # Вызвать стандартный метод удаления для удаления объекта поставщика

        return Response(
            {'detail': f'Индивидуальный предприниматель \'{vendor.title}\' '
                       f'и связанные с ним контакты были успешно удалены'},
            status=status.HTTP_204_NO_CONTENT)
