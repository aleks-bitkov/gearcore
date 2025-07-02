from django.db.models import Prefetch

from gearcore.carts.models import Cart
from gearcore.goods.models import VariantImage


def get_user_carts(request):
    if request.user.is_authenticated:
        return (
            Cart.objects.filter(user=request.user)
            .select_related("product", "variant")
            .prefetch_related("variant__images")  # Просто префетчим все изображения
        )

    if not request.session.session_key:
        request.session.create()
    return (
        Cart.objects.filter(session_key=request.session.session_key)
        .select_related("product", "variant")
        .prefetch_related(
            Prefetch("variant__images", queryset=VariantImage.objects.filter(is_main=True), to_attr="main_image_list"),
        )
    )
