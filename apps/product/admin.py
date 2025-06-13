from django.contrib import admin
from apps.product.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ("sku", "slug", "created", "updated")  # <-- Agregado slug
    list_display = ('name', 'sku', 'price', 'category', 'gender', 'active', 'created')
    search_fields = ('name', 'sku', 'slug')  # <-- Opcional, permite buscar por slug
    list_filter = ('category', 'gender', 'active')
