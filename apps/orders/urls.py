from django.urls import path
from .views import checkout_view, checkout_success_view, subir_comprobante_view

app_name = "orders"

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/success/', checkout_success_view, name='checkout_success'),
    path('subir-comprobante/<str:order_number>/', subir_comprobante_view, name='subir_comprobante'),
]