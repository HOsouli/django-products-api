from django.contrib import admin
from .models import Product


@admin.register(Product)
class Product_admin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "brand",
        "price",
        "stock",
        "published_date",
        "slug",
    )
    list_filter = ("category", "brand", "stock")
    search_fields = ("name", "brand", "category")


