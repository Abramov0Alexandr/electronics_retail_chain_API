from rest_framework import serializers
from products.models import Products


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания нового объекта модели Products
    """

    class Meta:
        model = Products
        fields = '__all__'
