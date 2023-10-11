from rest_framework import serializers
from products.models import Products


class ProductSerializer(serializers.ModelSerializer):

    manufacturer = serializers.CharField(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'
