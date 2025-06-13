from django.urls import path
from . import views

urlpatterns = [
    path('<str:genero>/', views.productos_por_genero, name='productos_genero'),
    path('<str:genero>/categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('detalles_producto/<slug:slug>/', views.detalles_producto, name='detalles_producto'),
]