from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import RetailChains
from suppliers.serializers import MainRetailChainsSerializer, RetailChainListSerializer
from suppliers.serializers.retail_chain_serializers import RetailChainUpdateSerializer


class RetailChainCreateApiView(generics.CreateAPIView):
    """
    Контроллер для публикации продукта.
    Доступ к контроллеру имеется только у суперпользователя и пользователей со статусом "Продавец".
    """

    serializer_class = MainRetailChainsSerializer


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

        retail_chain = self.get_object()  # Получаем объект розничной сети
        contacts = retail_chain.contacts  # Получаем связанные с объектом контакты

        if contacts:  # Удаляем связанные контакты
            contacts.delete()

        self.perform_destroy(retail_chain)  # Вызываем стандартный метод удаления для розничной сети

        # Возвращаем успешный ответ
        return Response(
            {'detail': f'Розничная сеть {retail_chain.title} и связанные с ней контакты были успешно удалены'},
            status=status.HTTP_204_NO_CONTENT)
