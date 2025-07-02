import json

from django.db.models import Exists
from django.db.models import OuterRef
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from gearcore.goods.models import Brand, Engine
from gearcore.goods.models import Category
from gearcore.goods.models import Motorcycle
from gearcore.goods.models import MotorcycleVariant
from gearcore.goods.models import VariantImage
from gearcore.goods.utils import q_search
from gearcore.wishlist.models import WishlistItem


class CatalogView(ListView):
    model = Motorcycle
    template_name = "goods/catalog.html"
    context_object_name = "products"
    paginate_by = 3

    def __init__(self):
        super().__init__()
        self.selected_categories = None
        self.selected_brands = None

    def get_queryset(self):
        filter_brands = self.request.GET.getlist("brand", "")
        filter_categories = self.request.GET.getlist("category", "")
        query = self.request.GET.get("q", None)

        if query:
            products = q_search(query)
        else:
            products = Motorcycle.objects.annotate(
                is_favorite=Exists(
                    WishlistItem.objects.filter(
                        wishlist__user=self.request.user,
                        product=OuterRef("pk"),
                    ),
                ),
            ).all()

        if filter_brands:
            products = super().get_queryset().filter(brand__slug__in=filter_brands)

        if filter_categories:
            products = products.filter(category__slug__in=filter_categories)

        self.selected_categories = filter_categories
        self.selected_brands = filter_brands

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "GearCore | Усі товари"
        context["brands"] = Brand.objects.all()
        context["categories"] = Category.objects.all()
        context["selected_categories"] = self.selected_categories
        context["selected_brands"] = self.selected_brands
        return context

catalog_view = CatalogView.as_view()


class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = "slug"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return Motorcycle.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"{self.object.name} | GearCore"
        motorcycle = self.object


        selected_variant = motorcycle.default_variant
        context["images"] = VariantImage.objects.filter(variant=selected_variant)
        context["variants"] = MotorcycleVariant.objects.filter(motorcycle=motorcycle)
        context["engine"] = Engine.objects.get(motorcycle=motorcycle)

        return context


product_view = ProductView.as_view()


class ProductColorChangeView(View):
    def post(self, request):
        data = json.loads(request.body)
        variant_id = data.get("variantId", -1)

        try:
            variant_id = int(variant_id)
        except ValueError:
            variant_id = -1

        if variant_id < 0:
            return JsonResponse(
                {"debug_message": "Не отримано ідентифіктор варіанту", "data": None}, status=400,
            )

        try:
            variants = VariantImage.objects.filter(variant=variant_id)
        except VariantImage.DoesNotExist:
            return JsonResponse(
                {"debug_message": f"не знайдено зображень для варіанту #{variant_id}", "data": None}, status=400,
            )

        images_info = []
        for variant in variants:
            images_info.append(variant.image.url)

        return JsonResponse({"debug_message": "дані отримані", "data": images_info}, status=200)

product_color_change_view = ProductColorChangeView.as_view()
