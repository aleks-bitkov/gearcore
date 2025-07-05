import json

from django.db.models import Exists
from django.db.models import OuterRef
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView

from gearcore.goods.models import Brand
from gearcore.goods.models import Category
from gearcore.goods.models import Engine
from gearcore.goods.models import Motorcycle
from gearcore.goods.models import MotorcycleVariant
from gearcore.goods.models import VariantImage
from gearcore.goods.utils import q_search
from gearcore.wishlist.models import Wishlist
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
        elif self.request.user.is_authenticated:
            products = Motorcycle.objects.annotate(
                is_favorite=Exists(
                    WishlistItem.objects.filter(
                        wishlist__user=self.request.user,
                        variant__motorcycle=OuterRef("pk"),
                    ),
                ),
            ).all()

        else:
            products = Motorcycle.objects.all()

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

        all_products = Motorcycle.objects.all()
        images = {}

        for product in all_products:
            variants = MotorcycleVariant.objects.filter(motorcycle=product)

            for variant in variants:
                variant_image = VariantImage.objects.get(variant=variant, is_main=True)
                try:
                    images[product.slug].append(variant_image)
                except KeyError:
                    images[product.slug] = []
                    images[product.slug].append(variant_image)

        wishlist_id = []
        try:
            wishlist = Wishlist.objects.get(user=self.request.user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
            wishlist_id = [item.variant.id for item in wishlist_items]
        except Wishlist.DoesNotExist:
            ...

        variants = MotorcycleVariant.objects.all()

        context["images"] = images
        context["variants"] = variants
        context["wishlist_id"] = wishlist_id
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
        wishlist_id = []
        try:
            wishlist = Wishlist.objects.get(user=self.request.user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
            wishlist_id = [item.variant.id for item in wishlist_items]
        except Wishlist.DoesNotExist:
            ...

        selected_variant = motorcycle.default_variant
        context["images"] = VariantImage.objects.filter(variant=selected_variant)
        context["variants"] = MotorcycleVariant.objects.filter(motorcycle=motorcycle)
        context["engine"] = Engine.objects.get(motorcycle=motorcycle)
        context["wishlist_id"] = wishlist_id

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
                {"debug_message": "Не отримано ідентифіктор варіанту", "data": None},
                status=400,
            )

        try:
            variants = VariantImage.objects.filter(variant=variant_id)
        except VariantImage.DoesNotExist:
            return JsonResponse(
                {"debug_message": f"не знайдено зображень для варіанту #{variant_id}", "data": None},
                status=400,
            )

        images_info = [variant.image.url for variant in variants]

        wishlist_id = []
        try:
            wishlist = Wishlist.objects.get(user=self.request.user)
            wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
            wishlist_id = [item.variant.id for item in wishlist_items]
        except Wishlist.DoesNotExist:
            ...

        return JsonResponse(
            {
                "debug_message": "дані отримані",
                "data": images_info,
                "wishlistId": wishlist_id,
            },
            status=200,
        )


product_color_change_view = ProductColorChangeView.as_view()
