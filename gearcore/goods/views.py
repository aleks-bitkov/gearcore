from django.shortcuts import render

from gearcore.goods.models import Products


# Create your views here.
def catalog(request):
    products = Products.objects.all()
    context = {
        "products": products,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, slug):
    return render(request, 'goods/product.html')
