from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions

from .models import Category, Product
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
    pagination_class = ProductPaginate
    permission_classes = [IsAdminOrReadOnly,]

    def get_queryset(self):
        return Product.objects.prefetch_related("category")

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer

        if self.request.method in ["POST", "PATCH"]:
            return AddProductSerializer

        return ProductSerializer
    
