from django.contrib import admin

from .models import Category, Product, Cart, CartItem, Order, OrderItem


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "price",
        "inventory",
        "invetory_status",
    ]
    list_editable = [
        "inventory",
    ]

    def invetory_status(self, product):
        return "LOW" if product.inventory < 10 else "HIGH"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 2


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["pk"]
    inlines = [
        CartItemInline,
    ]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 2


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["pk", "status", "customer", "total_price"]
    inlines = [
        OrderItemInline,
    ]
