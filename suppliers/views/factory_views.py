from rest_framework import generics, status
from rest_framework.response import Response
from suppliers.models import Factory
from suppliers.serializers import MainFactorySerializer, FactoryDetailSerializer
from suppliers.serializers.factory_serializers import FactoryUpdateSerializer


class FactoryCreateApiView(generics.CreateAPIView):
    """
    Контроллер для публикации продукта.
    Доступ к контроллеру имеется только у суперпользователя и пользователей со статусом "Продавец".
    """

    serializer_class = MainFactorySerializer


class FactoryListAPIView(generics.ListAPIView):
    queryset = Factory.objects.all()
    serializer_class = FactoryDetailSerializer


class FactoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Factory.objects.all()
    serializer_class = FactoryUpdateSerializer


class FactoryDeleteAPIView(generics.DestroyAPIView):
    """
    Удаляет и сам объект модели Factory и связанные с ним контакты
    """

    queryset = Factory.objects.all()

    def delete(self, request, *args, **kwargs):

        factory = self.get_object()  # Получаем объект завода
        contacts = factory.contacts  # Получаем связанные с объектом контакты

        if contacts:  # Удаляем связанные контакты
            contacts.delete()

        self.perform_destroy(factory)  # Вызываем стандартный метод удаления для завода

        # Возвращаем успешный ответ
        return Response({'detail': f'Завод {factory.title} и связанные с ним контакты были успешно удалены'},
                        status=status.HTTP_204_NO_CONTENT)
