from django.contrib import admin
from apps.product.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("sku", "slug", "created", "updated")
    list_display = ('name', 'sku', 'price', 'stock' , 'category', 'gender', 'active', 'created', 'updated')
    search_fields = ('name', 'sku', 'slug')  # <-- permite buscar por
    list_filter = ('category', 'gender', 'active', 'price')
