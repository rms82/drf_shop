from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import DjangoModelPermissions

from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product
from .filters import ProductFilterSet
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    AddProductSerializer,
    ProductSerializer,
)
from .paginations import ProductPaginate
from .permissions import IsAdminOrReadOnly


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = ProductPaginate

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilterSet
    search_fields = ["title"]
    ordering_fields = ["updated_at", "price"]

    def get_queryset(self):
        return Product.objects.prefetch_related("category")

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.request.method in ["POST", "PATCH"]:
            return AddProductSerializer

        return ProductSerializer
