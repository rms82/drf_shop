from django.db import models
from django.utils.text import slugify

from uuid import uuid4

from accounts.models import ProfileUser


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    image = models.ImageField(upload_to="product/img/", null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveSmallIntegerField(default=0)
    category = models.ManyToManyField(Category, related_name="products", blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(obj, *args, **kwargs):
        obj.slug = slugify(obj.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} - {self.inventory}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart id: {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (
            "cart",
            "product",
        )


class Order(models.Model):
    STATUS_UNPAID = "u"
    STATUS_PAID = "p"
    STATUS_CANSELLED = "c"
    STATUS = (
        (STATUS_UNPAID, "Unpaid"),
        (STATUS_PAID, "Paid"),
        (STATUS_CANSELLED, "Canselled"),
    )

    customer = models.ForeignKey(
        ProfileUser, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(max_length=2, choices=STATUS, default=STATUS_UNPAID)
    total_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart id: {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderitems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = (
            "order",
            "product",
        )
