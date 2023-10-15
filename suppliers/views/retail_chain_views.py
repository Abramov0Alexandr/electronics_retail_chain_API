from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import RetailChains
from suppliers.serializers import RetailChainSerializer, RetailChainSupplierSerializer, RetailChainListSerializer
from suppliers.serializers.retail_chain_serializers import RetailChainUpdateSerializer


class RetailChainCreateApiView(generics.CreateAPIView):
    """
.
    """

    def get_serializer_class(self):

        supplier_content_type_choice = self.request.data.get('supplier_content_type')
        supplier_id = self.request.data.get('supplier_id')

        if supplier_content_type_choice and supplier_id:
            return RetailChainSupplierSerializer

        else:
            return RetailChainSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetailChainListApiView(generics.ListAPIView):
    queryset = RetailChains.objects.all()
    serializer_class = RetailChainListSerializer


class RetailChainUpdateAPIView(generics.UpdateAPIView):

    queryset = RetailChains.objects.all()
    serializer_class = RetailChainUpdateSerializer


class RetailChainDeleteAPIView(generics.DestroyAPIView):
    """
    Удаляет и сам объект модели RetailChain и связанные с ним контакты
    """

    queryset = RetailChains.objects.all()

    def delete(self, request, *args, **kwargs):

        retail_chain = self.get_object()  # Получить объект розничной сети
        contacts = retail_chain.contacts  # Получить связанные с объектом контакты

        if contacts:  # Удалить связанные контакты
            contacts.delete()

        self.perform_destroy(retail_chain)  # Вызвать стандартный метод удаления для розничной сети

        # Вернуть успешный ответ
        return Response(
            {'detail': f'Розничная сеть {retail_chain.title} и связанные с ней контакты были успешно удалены'},
            status=status.HTTP_204_NO_CONTENT)
