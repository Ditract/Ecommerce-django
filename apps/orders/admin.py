from django.contrib import admin
from .models import Order, OrderItem, Payment

# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('number', 'user', 'status', 'total', 'created_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'method', 'status', 'paid_at')
    readonly_fields = ('comprobante',)
