from django.shortcuts import render
from .models import Slide
from ..product.models import Product


# Create your views here.
def home(request):
    context = {'slides': Slide.objects.filter(active=True).order_by('order'),
               'ultimos_4_productos': Product.objects.all().order_by('-created')[:4]
               }
    return render(request, "pages/index.html", context)