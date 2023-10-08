from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "title"]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    num_of_category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "pk",
            "title",
            "slug",
            "image",
            "price",
            "inventory",
            'num_of_category', 
            "category",
        ]

    def get_num_of_category(self, product):
        return product.category.count()

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'pk',
            "title",
            "image",
            "description",
            "price",
            "inventory",
            "category",
            "created_at",
            "updated_at",
        ]


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "image",
            "description",
            "price",
            "inventory",
            "category",
        ]
