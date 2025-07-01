import json

from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.views import View
from django.db.models import Exists, OuterRef

from gearcore.goods.models import Motorcycle, Category, Brand, VariantImage, MotorcycleVariant
from gearcore.goods.utils import q_search
from gearcore.wishlist.models import WishlistItem


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
            products = Motorcycle.objects.annotate(
                is_favorite=Exists(
                    WishlistItem.objects.filter(
                        wishlist__user=self.request.user,
                        product=OuterRef('pk')
                    )
                )
            ).all()

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
        context["brands"] = Brand.objects.all()
        context["categories"] = Category.objects.all()
        context["selected_categories"] = self.selected_categories
        context["selected_brands"] = self.selected_brands
        return context

catalog_view = CatalogView.as_view()

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
        motorcycle = self.object

        print(f'\n\n\n\n\n{motorcycle=}\n\n\n\n\n\n')
        # available_variants = motorcycle.variants.filter(is_available=True).select_related('color')
        selected_variant = motorcycle.default_variant
        context['images'] = VariantImage.objects.filter(variant=selected_variant)
        return context


product_view = ProductView.as_view()


class ProductColorChangeView(View):
    def post(self, request):
        data = json.loads(request.body)
        color_id = data.get('colorId', -1)
        product_slug = data.get('productSlug', '')

        if color_id < 0:
            return JsonResponse({'debug_message': 'Не отримано ідентифіктор кольору'}, status=400)

        if not product_slug:
            return JsonResponse({'debug_message': 'Не отримано slug продукту'}, status=400)

        try:
            motorcycle = Motorcycle.objects.get(slug=product_slug)
        except Motorcycle.DoesNotExist:
            return JsonResponse({'debug_message': 'такого продукту не існує'}, status=400)


        available_variants = motorcycle.variants.filter(is_available=True).select_related('color')
        selected_variant = motorcycle.default_variant

        try:
            selected_variant = available_variants.get(color__id=color_id)
        except MotorcycleVariant.DoesNotExist:
            return JsonResponse({'debug_message': 'не знайдено обраний варіант за кольором'}, status=400)

        images = VariantImage.objects.filter(variant=selected_variant)

        image_data = [
            {
                'id': image.id,
                'url': image.image.url,
                'title': image.title,
                'is_main': image.is_main,
                'sort_order': image.sort_order,
            }
            for image in images
        ]

        return JsonResponse({'images': image_data}, status=200)

product_color_change_view = ProductColorChangeView.as_view()

# def product(request, slug):
#     product_item = Products.objects.get(slug=slug)
#
#     context = {
#         "product": product_item,
#     }
#
#     return render(request, 'goods/product.html', context)
