from rest_framework import serializers
from products.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(  # для визуальной проверки на этапе разработки
        source='parent.name', allow_null=True
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'parent', 'parent_name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'image_small', 'image_medium', 'image_large', 'price', 'category']
