from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category

# Mapeo URL -> Código interno en modelo
GENERO_MAP_URL_TO_CODE = {
    'hombre': 'M',
    'mujer': 'F',
    'unisex': 'U',
}

# Mapeo código interno -> Nombre legible para título/etiquetas
GENERO_MAP_CODE_TO_NOMBRE = {
    'M': 'Hombre',
    'F': 'Mujer',
    'U': 'Unisex',
}


def productos_por_genero(request, genero):
    genero_lower = genero.lower()
    gender_code = GENERO_MAP_URL_TO_CODE.get(genero_lower, 'U')

    # Obtenemos los productos activos para ese género
    productos_qs = Product.objects.filter(gender=gender_code, active=True)

    # Obtenemos las categorías activas (sidebar)
    categorias = Category.objects.filter(active=True)

    # --- Paginación ---
    paginator = Paginator(productos_qs, 6)  # 6 productos por página
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    context = {
        'productos': productos,
        'titulo': f'Zapatos para {GENERO_MAP_CODE_TO_NOMBRE.get(gender_code, "Otro")}',
        'categorias': categorias,
        'genero_actual': genero_lower,
        'genero_codigo': gender_code,
        'genero_nombre': GENERO_MAP_CODE_TO_NOMBRE.get(gender_code, "Otro"),
    }
    return render(request, "product/listado.html", context)


def productos_por_categoria(request, genero, categoria_id):
    genero_lower = genero.lower()
    gender_code = GENERO_MAP_URL_TO_CODE.get(genero_lower, 'U')

    # Obtenemos la categoría seleccionada
    categoria = get_object_or_404(Category, id=categoria_id, active=True)

    # Filtramos productos por categoría, género y activos
    productos_qs = Product.objects.filter(category=categoria, gender=gender_code, active=True)
    categorias = Category.objects.filter(active=True)

    # --- Paginación ---
    paginator = Paginator(productos_qs, 6)  # 6 productos por página (igual que en productos_por_genero)
    page = request.GET.get('page')

    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    context = {
        'productos': productos,
        'titulo': f'Zapatos para {GENERO_MAP_CODE_TO_NOMBRE.get(gender_code, "Otro")} - Categoría: {categoria.name}',
        'categorias': categorias,
        'categoria_actual': categoria,
        'genero_actual': genero_lower,
        'genero_codigo': gender_code,
        'genero_nombre': GENERO_MAP_CODE_TO_NOMBRE.get(gender_code, "Otro"),
    }
    return render(request, 'product/listado.html', context)


def detalles_producto(request, slug):
    producto = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'product/detalles_producto.html', {'producto': producto})