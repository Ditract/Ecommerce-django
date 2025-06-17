# apps/orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment

@receiver(post_save, sender=Payment)
def actualizar_estado_pedido(sender, instance, **kwargs):
    order = instance.order
    pago_status = instance.status

    if pago_status == 'COM':
        order.status = 'PRO'  # o 'ENV' si prefieres
    elif pago_status in ['FAL', 'DEV']:
        order.status = 'CAN'
    else:
        # Si el estado del pago es 'PEN', mantenemos el estado del pedido como está
        return

    order.save()
