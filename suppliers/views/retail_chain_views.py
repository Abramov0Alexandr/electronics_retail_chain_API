from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import RetailChains
from suppliers import serializers


class RetailChainCreateApiView(generics.CreateAPIView):
    """
    Контроллер для создания нового объекта модели RetailChains.
    """

    def get_serializer_class(self):
        """
        Метод для определения будет ли создаваться объект без поставщика или с поставщиком.
        :return: Сериализатор для создания объекта модели RetailChains.
        """

        supplier_content_type_choice = self.request.data.get('supplier_content_type')
        supplier_id = self.request.data.get('supplier_id')

        if supplier_content_type_choice and supplier_id:
            return serializers.RetailChainSupplierSerializer

        else:
            return serializers.RetailChainSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetailChainListApiView(generics.ListAPIView):
    """
    Контроллер для получения списка объектов модели RetailChains.
    """

    queryset = RetailChains.objects.all()
    serializer_class = serializers.RetailChainListSerializer


class RetailChainUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования объекта модели RetailChains.
    """

    queryset = RetailChains.objects.all()
    serializer_class = serializers.RetailChainUpdateSerializer


class RetailChainDeleteAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели RetailChains.
    Контроллер одновременно с удалением объект поставщика, удаляет и связанные с ним контакты.
    """

    queryset = RetailChains.objects.all()

    def delete(self, request, *args, **kwargs):

        retail_chain = self.get_object()  # Получить объект поставщика
        contacts = retail_chain.contacts  # Получить связанные с объектом контакты

        if contacts:  # Удалить связанные контакты
            contacts.delete()

        self.perform_destroy(retail_chain)  # Вызвать стандартный метод удаления для удаления объекта поставщика

        return Response(
            {'detail': f'Розничная сеть {retail_chain.title} и связанные с ней контакты были успешно удалены'},
            status=status.HTTP_204_NO_CONTENT)
