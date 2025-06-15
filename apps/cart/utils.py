from .models import Cart


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    else:
        if not request.session.session_key:
            request.session.create()  # asegura que tenga una sesión
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key, active=True)
    return cart
