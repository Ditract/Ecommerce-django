from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.product.models import Product
from .models import Cart, CartItem
from .utils import get_or_create_cart


def cart_detail(request):
    #cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    cart = get_or_create_cart(request)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'cart/cart_sidebar.html', {'cart': cart})

    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    #cart, _ = Cart.objects.get_or_create(user=request.user, active=True)
    cart = get_or_create_cart(request)

    #  Leer cantidad del formulario o usar 1 por defecto
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1

    # 🔍 Buscar o crear el item en el carrito
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price': product.price, 'quantity': 0}
    )

    #  Calcular nueva cantidad total
    new_quantity = cart_item.quantity + quantity if not item_created else quantity

    #  Validar stock
    if new_quantity > product.stock:
        error_msg = f"Stock insuficiente. Solo quedan {product.stock} unidades."

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_msg,
                'cart_total': cart.total(),
                'cart_items': cart.items.count()
            })
        else:
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', 'product_list'))

    #  Guardar la nueva cantidad
    cart_item.quantity = new_quantity
    cart_item.save()

    #  Devolver respuesta
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total(),
            'cart_items': cart.items.count()
        })

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))



def cart_remove(request, item_id):
    #cart = get_object_or_404(Cart, user=request.user, active=True)
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total(),
            'cart_items': cart.items.count()
        })

    return redirect('cart:cart_detail')


from django.views.decorators.http import require_POST
from django.contrib import messages



@require_POST
def cart_update(request, item_id):
    #cart = get_object_or_404(Cart, user=request.user, active=True)
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product = cart_item.product  # Necesario para validar el stock

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        cart_item.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart.total(),
                'cart_items': cart.items.count()
            })

        return redirect('cart:cart_detail')

    #  Validar stock
    if quantity > product.stock:
        error_msg = f"¡Perdón! :( Solo quedan {product.stock} unidades."
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': error_msg,
                'item_id': item_id,
                'cart_total': cart.total(),
                'cart_items': cart.items.count()
            })
        else:
            messages.error(request, error_msg)
            return redirect('cart:cart_detail')

    # Guardar nueva cantidad
    cart_item.quantity = quantity
    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total(),
            'cart_items': cart.items.count()
        })

    return redirect('cart:cart_detail')
