"""
Views para el manejo de órdenes y pagos.
Incluye checkout, subida de comprobantes y confirmación de compra.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem, Payment
from .forms import AddressForm, PaymentForm, ComprobanteForm
from .utils import generar_numero_unico

# Configurar logging
logger = logging.getLogger(__name__)


@login_required
@transaction.atomic
def checkout_view(request):
    """
    Vista para procesar el checkout del carrito de compras.

    Funcionalidad:
    - Valida que el usuario tenga items en el carrito
    - Crea o reutiliza una orden pendiente
    - Maneja direcciones de envío
    - Crea pagos de forma segura evitando duplicados
    - Limpia el carrito tras completar el proceso

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Renderiza checkout.html o redirige según el resultado
    """
    user = request.user

    # Verificar que el usuario tenga un carrito con items
    try:
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            messages.warning(request, 'Tu carrito está vacío.')
            return redirect('cart:cart_detail')
    except Cart.DoesNotExist:
        messages.warning(request, 'No tienes un carrito activo.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if address_form.is_valid() and payment_form.is_valid():
            try:
                # Buscar orden pendiente existente para evitar duplicados
                order = Order.objects.filter(
                    user=user,
                    status='PEN'
                ).order_by('-created_at').first()

                # Crear nueva orden si no existe una pendiente
                if not order:
                    order = _create_new_order(user, cart, address_form)
                    logger.info(f"Nueva orden creada: {order.number} para usuario {user.username}")

                # Crear o obtener pago pendiente (evita duplicados con UniqueConstraint)
                payment, payment_created = Payment.objects.get_or_create(
                    order=order,
                    status='PEN',
                    defaults={
                        'amount': order.total,
                        'method': payment_form.cleaned_data['method'],
                    }
                )

                if payment_created:
                    # Solo vaciar carrito cuando se crea un nuevo pago
                    cart.items.all().delete()
                    logger.info(f"Carrito vaciado para usuario {user.username}")
                    messages.success(request, 'Orden creada exitosamente.')
                else:
                    # Actualizar método de pago si cambió
                    if payment.method != payment_form.cleaned_data['method']:
                        payment.method = payment_form.cleaned_data['method']
                        payment.save()
                    messages.info(request, 'Continuando con orden existente.')

                return redirect('orders:subir_comprobante', order_number=order.number)

            except ValidationError as e:
                logger.error(f"Error de validación en checkout: {e}")
                messages.error(request, 'Error al procesar la orden. Inténtalo de nuevo.')
            except Exception as e:
                logger.error(f"Error inesperado en checkout: {e}")
                messages.error(request, 'Ocurrió un error inesperado. Contacta soporte.')

    else:
        address_form = AddressForm()
        payment_form = PaymentForm()

    context = {
        'cart': cart,
        'address_form': address_form,
        'payment_form': payment_form,
        'shipping_cost': 8000,  # Centralizar costo de envío
    }
    return render(request, 'orders/checkout.html', context)


def _create_new_order(user, cart, address_form):
    """
    Función auxiliar para crear una nueva orden con sus items.

    Args:
        user: Usuario que hace la orden
        cart: Carrito con los productos
        address_form: Formulario validado con la dirección

    Returns:
        Order: Nueva orden creada
    """
    # Crear y guardar dirección
    address = address_form.save(commit=False)
    address.user = user
    address.save()

    # Crear orden
    shipping_cost = 8000  # Centralizar costo de envío
    order = Order.objects.create(
        user=user,
        number=generar_numero_unico(),
        subtotal=cart.total(),
        shipping_cost=shipping_cost,
        total=cart.total() + shipping_cost,
        shipping_address=address,
    )

    # Crear items de la orden
    order_items = []
    for cart_item in cart.items.select_related('product'):
        order_items.append(OrderItem(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            unit_price=cart_item.product.price,
            subtotal=cart_item.subtotal(),
        ))

    # Bulk create para mejor rendimiento
    OrderItem.objects.bulk_create(order_items)

    return order


@login_required
def subir_comprobante_view(request, order_number):
    """
    Vista para subir comprobante de pago de una orden.

    Funcionalidad:
    - Valida que la orden pertenezca al usuario
    - Obtiene el pago pendiente asociado
    - Permite actualizar comprobante y método de pago
    - Cambia el estado de la orden a 'Procesando'

    Args:
        request: HttpRequest object
        order_number: Número único de la orden

    Returns:
        HttpResponse: Renderiza subir_comprobante.html o redirige al éxito
    """
    # Obtener orden y validar pertenencia al usuario
    order = get_object_or_404(Order, number=order_number, user=request.user)

    # Verificar que la orden esté en estado válido para subir comprobante
    if order.status not in ['PEN', 'PRO']:
        messages.error(request, 'Esta orden no puede ser modificada.')
        return redirect('orders:order_detail', order_number=order_number)

    try:
        # Obtener el pago pendiente (debe existir tras checkout)
        payment = Payment.objects.get(order=order, status='PEN')
    except Payment.DoesNotExist:
        logger.error(f"No se encontró pago pendiente para orden {order_number}")
        messages.error(request, 'No se encontró información de pago para esta orden.')
        return redirect('orders:checkout_success')

    if request.method == 'POST':
        form = ComprobanteForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                # Actualizar pago existente
                payment.comprobante = form.cleaned_data['comprobante']

                # Actualizar método si se proporcionó
                if 'method' in form.cleaned_data and form.cleaned_data['method']:
                    payment.method = form.cleaned_data['method']

                payment.save()

                # Actualizar estado de la orden
                order.status = 'PRO'  # Procesando
                order.save()

                logger.info(f"Comprobante subido para orden {order_number}")
                messages.success(request, 'Comprobante subido exitosamente. Tu orden está siendo procesada.')

                return redirect('orders:checkout_success')

            except Exception as e:
                logger.error(f"Error al subir comprobante para orden {order_number}: {e}")
                messages.error(request, 'Error al procesar el comprobante. Inténtalo de nuevo.')
    else:
        # Pre-llenar formulario con datos existentes
        initial_data = {'method': payment.method}
        form = ComprobanteForm(initial=initial_data)

    context = {
        'form': form,
        'order': order,
        'payment': payment,
        'can_change_method': True,  # Permitir cambio de método en esta etapa
    }
    return render(request, 'orders/subir_comprobante.html', context)


@login_required
def checkout_success_view(request):
    """
    Vista de confirmación tras completar el proceso de checkout.

    Muestra mensaje de éxito y próximos pasos al usuario.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse: Renderiza checkout_success.html
    """
    # Opcional: Obtener la última orden del usuario para mostrar detalles
    latest_order = Order.objects.filter(
        user=request.user,
        status__in=['PRO', 'PEN']
    ).order_by('-created_at').first()

    context = {
        'latest_order': latest_order,
        'support_email': 'soporte@tutienda.com',  # Centralizar contacto
    }
    return render(request, 'orders/checkout_success.html', context)