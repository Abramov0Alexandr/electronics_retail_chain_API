from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import Factory
from suppliers import serializers


class FactoryCreateApiView(generics.CreateAPIView):
    """
    Контроллер для создания нового объекта модели Factory.
    """

    serializer_class = serializers.FactoryCreateSerializer


class FactoryListAPIView(generics.ListAPIView):
    """
    Контроллер для получения списка объектов модели Factory.
    """

    queryset = Factory.objects.all()
    serializer_class = serializers.FactoryDetailSerializer


class FactoryUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования объекта модели Factory.
    """

    queryset = Factory.objects.all()
    serializer_class = serializers.FactoryUpdateSerializer


class FactoryDeleteAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели Factory.
    Контроллер одновременно с удалением объект поставщика, удаляет и связанные с ним контакты.
    """

    queryset = Factory.objects.all()

    def delete(self, request, *args, **kwargs):

        factory = self.get_object()  # Получить объект поставщика
        contacts = factory.contacts  # Получить связанные с объектом контакты

        if contacts:  # Удалить связанные контакты
            contacts.delete()

        self.perform_destroy(factory)  # Вызвать стандартный метод удаления для удаления объекта поставщика

        return Response({'detail': f'Завод {factory.title} и связанные с ним контакты были успешно удалены'},
                        status=status.HTTP_204_NO_CONTENT)
