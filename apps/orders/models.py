from django.db import models
from django.conf import settings

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('PEN', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    number = models.CharField(max_length=20, unique=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    shipping_address = models.ForeignKey('shipping.Address', on_delete=models.PROTECT, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido #{self.number} - {self.user.username}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle del pedido'
        verbose_name_plural = 'Detalles del pedido'

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Pedido #{self.order.number})"



class Payment(models.Model):
    METHOD_CHOICES = [
        ('NEQUI', 'Nequi'),
        ('DAVIPLATA', 'Daviplata'),
        ('BANK', 'Transferencia Bancaria'),
    ]

    STATUS_CHOICES = [
        ('PEN', 'Pendiente'),
        ('COM', 'Completado'),
        ('FAL', 'Fallido'),
        ('DEV', 'Devuelto'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    paid_at = models.DateTimeField(auto_now_add=True)
    comprobante = models.ImageField(upload_to='comprobantes/%Y/%m/%d/', null=True, blank=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        # NUEVA RESTRICCIÓN: Solo un pago pendiente por orden
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'status'],
                condition=models.Q(status='PEN'),
                name='unique_pending_payment_per_order'
            )
        ]

    def __str__(self):
        return f"{self.get_method_display()} - {self.amount} COP - {self.get_status_display()}"
