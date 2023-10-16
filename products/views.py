from rest_framework import generics
from products.models import Products
from products.serializers import ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания нового объекта модели Products.
    """

    serializer_class = ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    """
    Контроллер получения списка объектов модели Products.
    """

    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class ProductUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для редактирования объекта модели Products.
    """

    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class ProductDeleteAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления объекта модели Products.
    """

    queryset = Products.objects.all()
