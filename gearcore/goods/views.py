from django.views.generic import DetailView, ListView

from gearcore.goods.models import Motorcycle, Categories, Brands
from gearcore.goods.utils import q_search


class CatalogView(ListView):
    model = Motorcycle
    template_name = "goods/catalog.html"
    context_object_name = "products"
    paginate_by = 3
    # allow_empty = False # raise 404

    def get_queryset(self):
        filter_brands = self.request.GET.getlist("brand", "")
        filter_categories = self.request.GET.getlist("category", "")
        query = self.request.GET.get('q', None)

        if query:
            products = q_search(query)
        else:
            products = Motorcycle.objects.prefetch_related("images").all()

        if filter_brands:
            products = super(CatalogView, self).get_queryset().filter(brand__slug__in=filter_brands)

        if filter_categories:
            products = products.filter(category__slug__in=filter_categories)

        self.selected_categories = filter_categories
        self.selected_brands = filter_brands

        return products

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)
        context["title"] = "GearCore | Усі товари"
        context["brands"] = Brands.objects.all()
        context["categories"] = Categories.objects.all()
        context["selected_categories"] = self.selected_categories
        context["selected_brands"] = self.selected_brands
        return context

catalog_view = CatalogView.as_view()


# def catalog(request):
#     page = request.GET.get('page', 1)
#     filter_categories = request.GET.getlist('category', None)
#     filter_brands = request.GET.getlist('brand', None)
#     query = request.GET.get('q', None)
#
#     if query:
#         products = q_search(query)
#     else:
#         products = Products.objects.all()
#
#     categories = Categories.objects.all()
#     brands = Brands.objects.all()
#
#     if filter_categories:
#         products = products.filter(category__slug__in=filter_categories)
#
#     if filter_brands:
#         products = products.filter(brand__slug__in=filter_brands)
#
#     paginator = Paginator(products, 3)
#     current_page = paginator.page(page)
#
#     context = {
#         "products": current_page,
#         "page_obj": current_page,
#         "categories": categories,
#         "brands": brands,
#         "selected_categories": filter_categories,
#         "selected_brands": filter_brands,
#     }
#     return render(request, 'goods/catalog.html', context)

class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = 'slug'
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = Motorcycle.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        context["title"] = f"{self.object.name} | GearCore"
        return context


product_view = ProductView.as_view()
# def product(request, slug):
#     product_item = Products.objects.get(slug=slug)
#
#     context = {
#         "product": product_item,
#     }
#
#     return render(request, 'goods/product.html', context)
