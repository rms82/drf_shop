from django_filters.rest_framework import FilterSet

from .models import Product


class ProductFilterSet(FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['gte', 'lte'],
            'inventory': ['gte', 'lte'],
            'category': ['exact'],

        }
