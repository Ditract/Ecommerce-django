from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from apps.product.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print("📦 Renderizando cart_sidebar.html")
        return render(request, 'cart/cart_sidebar.html', {'cart': cart})

    print("🖥️ Renderizando cart_detail.html")
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'price': product.price}
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total(),
            'cart_items': cart.items.count()
        })

    return redirect(request.META.get('HTTP_REFERER',
                                     'product_list'))  # Cambia 'product_list' por el nombre de tu vista de productos


@login_required
def cart_remove(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, active=True)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_total': cart.total(),
            'cart_items': cart.items.count()
        })

    return redirect('cart:cart_detail')


@login_required
def cart_update(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, active=True)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'cart_total': cart.total(),
                'cart_items': cart.items.count()
            })

    return redirect('cart:cart_detail')