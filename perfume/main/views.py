from django.shortcuts import render
from .models import Product, ProductVolume

# Create your views here.
def MainView(request):
    products = Product.objects.all().filter(active=True)
    return render(request, "main/index.html", {
        'products': products,
    })