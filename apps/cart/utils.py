from .models import Cart

#Obtener carrito del usuario autenticado
def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user, active=True)
    return cart