from django.db import models
from django.conf import settings
from apps.product.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'


    def __str__(self):
        return f"Carrito #{self.id} de {self.user.username} - {'Activo' if self.active else 'Inactivo'}"


    def total(self):
        return sum(item.subtotal() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Detalle del carrito'
        verbose_name_plural = 'Detalles del carrito'
        unique_together = ('cart', 'product') #No duplicar producto en el mismo carrito

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en Carrito #{self.cart.id}"

    def subtotal(self):
        return self.quantity * self.price