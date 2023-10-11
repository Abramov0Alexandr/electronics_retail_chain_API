from rest_framework import generics
from products.models import Products
from products.serializers import ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class ProductUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()


class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Products.objects.all()
