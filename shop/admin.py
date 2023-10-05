from django.contrib import admin

from .models import Categoty, Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'inventory']
    