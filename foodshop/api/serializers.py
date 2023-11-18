from rest_framework import serializers
from products.models import Category, Product, Cart


class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(  # для визуальной проверки на этапе разработки
        source='parent.name', allow_null=True
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'parent', 'parent_name']


class ProductsSerializer(serializers.ModelSerializer):
    parent_category_id = serializers.CharField(source='category.parent.id', read_only=True, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'parent_category_id', 'price', 'image_large', 'image_medium', 'image_small'
        ]


class CartSerializer(serializers.ModelSerializer):
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['product', 'product_price', 'quantity']

    def get_product_price(self, obj):
        return obj.product.price
