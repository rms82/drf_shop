from rest_framework import serializers

from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["pk", "title"]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "pk",
            "title",
            "slug",
            "image",
            "price",
            "inventory",
            "category",
        ]


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
