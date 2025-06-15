from django.core.paginator import Paginator
from django.shortcuts import render

from gearcore.goods.models import Products, Categories, Brands
from gearcore.goods.utils import q_search


# Create your views here.
def catalog(request):
    page = request.GET.get('page', 1)
    filter_categories = request.GET.getlist('category', None)
    filter_brands = request.GET.getlist('brand', None)
    query = request.GET.get('q', None)

    if query:
        products = q_search(query)
    else:
        products = Products.objects.all()

    categories = Categories.objects.all()
    brands = Brands.objects.all()

    if filter_categories:
        products = products.filter(category__slug__in=filter_categories)

    if filter_brands:
        products = products.filter(brand__slug__in=filter_brands)

    paginator = Paginator(products, 3)
    current_page = paginator.page(page)

    context = {
        "products": current_page,
        "page_obj": current_page,
        "categories": categories,
        "brands": brands,
        "selected_categories": filter_categories,
        "selected_brands": filter_brands,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, slug):
    product_item = Products.objects.get(slug=slug)

    context = {
        "product": product_item,
    }

    return render(request, 'goods/product.html', context)
