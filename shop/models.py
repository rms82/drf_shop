from django.db import models
from django.utils.text import slugify

from django.utils.text import slugify


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
