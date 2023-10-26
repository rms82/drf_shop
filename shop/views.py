from django.db.models import Prefetch

from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import (
    DjangoModelPermissions,
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response


from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .filters import ProductFilterSet
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    AddProductSerializer,
    ProductSerializer,
    UpdateProductSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    OrderSerializer,
    OrderAdminSerializer,
    AddOrderSerializer,
    UpdateOrderSerializer,
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

        if self.request.method == "PATCH":
            return UpdateProductSerializer

        if self.request.method == "POST":
            return AddProductSerializer

        return ProductSerializer


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.prefetch_related(
            Prefetch("items", queryset=CartItem.objects.select_related("product"))
        )


class CartItemViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_pk")
        return CartItem.objects.filter(cart_id=cart_id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer

        if self.request.method == "PATCH":
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs.get("cart_pk")}

    def get_permissions(self):
        return [
            AllowAny(),
        ]


class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        queryset = (
            Order.objects.prefetch_related(
                Prefetch(
                    "orderitems", queryset=OrderItem.objects.select_related("product")
                )
            )
            .select_related("customer__user")
            .all()
        )
        if self.request.user.is_staff:
            return queryset

        return queryset.filter(customer__user_id=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddOrderSerializer

        if self.request.method == "PATCH":
            return UpdateOrderSerializer

        if self.request.user.is_staff:
            return OrderAdminSerializer

        return OrderSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.pk}

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [
                IsAdminUser(),
            ]

        return [
            IsAuthenticated(),
        ]

    def create(self, request, *args, **kwargs):
        serializer = AddOrderSerializer(
            data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)
