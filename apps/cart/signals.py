from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver
from .models import Cart, CartItem


@receiver(user_logged_in)
def merge_carts_on_login(sender, request, user, **kwargs):
    print("✅ Señal user_logged_in activada")

    #  Recuperar la session_key antes de login
    old_session_key = request.session.get('pre_login_session_key')
    print("Pre-login session key:", old_session_key)

    if not old_session_key:
        print("⚠No se pudo recuperar la session_key anterior")
        return

    try:
        session_cart = Cart.objects.get(session_key=old_session_key, active=True, user__isnull=True)
        print("Carrito anónimo encontrado:", session_cart.id)
    except Cart.DoesNotExist:
        print("No se encontró carrito anónimo con esa session_key")
        return

    # Buscar carrito del usuario logueado
    user_cart, created = Cart.objects.get_or_create(user=user, active=True)

    # Mover los ítems del carrito anónimo al del usuario
    for item in session_cart.items.all():
        user_item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=item.product,
            defaults={'price': item.price, 'quantity': 0}
        )
        user_item.quantity += item.quantity
        user_item.save()

    # Desactivar el carrito anónimo
    session_cart.active = False
    session_cart.save()
    print("Carrito fusionado con éxito")
