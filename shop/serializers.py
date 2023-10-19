from django.db import transaction

from rest_framework import serializers

from .models import Product, Category, Cart, CartItem, Order, OrderItem
from accounts.models import ProfileUser


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
            "num_of_category",
            "category",
        ]

    def get_num_of_category(self, product):
        return product.category.count()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "pk",
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


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "price",
            "inventory",
        ]


class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["pk", "title", "price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def check_quantity(self, quantity, inventory):
        if quantity > inventory:
            raise serializers.ValidationError(
                {"detail": "quantity must be less than inventory"}
            )

    def create(self, validated_data):
        with transaction.atomic():
            cart_id = self.context.get("cart_id")
            quantity = self.validated_data.get("quantity")
            product = self.validated_data.get("product")

            try:
                cartitem = CartItem.objects.get(cart_id=cart_id, product=product)
                cartitem.quantity += quantity
                self.check_quantity(
                    quantity=cartitem.quantity, inventory=product.inventory
                )
                cartitem.save()

            except CartItem.DoesNotExist:
                self.check_quantity(quantity=quantity, inventory=product.inventory)
                cartitem = CartItem.objects.create(cart_id=cart_id, **validated_data)

            self.instance = cartitem
            return cartitem


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product = ProductCartItemSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, cartitem: CartItem):
        return cartitem.quantity * cartitem.product.price


class CartSerializer(serializers.ModelSerializer):
    total_cart_price = serializers.SerializerMethodField()
    items = CartItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items_count", "items", "total_cart_price"]

    def get_total_cart_price(self, cart: Cart):
        return sum(item.quantity * item.product.price for item in cart.items.all())

    def get_items_count(self, cart: Cart):
        return cart.items.count()


class ProfileOrderSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = ProfileUser
        fields = ["pk", "user", "username", "fullname"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = OrderItem
        fields = ["product", "quantity",]


class OrderAdminSerializer(serializers.ModelSerializer):
    customer = ProfileOrderSerializer(read_only=True)
    orderitems = OrderItemSerializer(many=True)


    class Meta:
        model = Order
        fields = ["pk", "customer", "status", "total_price", "orderitems"]


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ["pk", "status", "total_price", "orderitems"]


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status",]


class AddOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField(required=True)

    def validate_cart_id(self, cart_id):
        try:
            cart = Cart.objects.get(pk=cart_id)
            if cart.items.count() == 0:
                raise serializers.ValidationError("cart is empty")

        except Cart.DoesNotExist:
            raise serializers.ValidationError("cart id is not valid")

        return cart_id

    def save(self, **kwargs):
        cart_id = self.validated_data.get("cart_id")

        user_id = self.context.get("user_id")
        user_profile = ProfileUser.objects.get(user_id=user_id)

        with transaction.atomic():
            order = Order()
            order.customer_id = user_profile.pk
            order.save()

            cart_items = CartItem.objects.filter(cart_id=cart_id)

            order_items = [
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                )
                for cart_item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.get(pk=cart_id).delete()

            return order
