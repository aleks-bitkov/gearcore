from django.template.loader import render_to_string
from django.urls import reverse

from gearcore.carts.models import Cart
from gearcore.carts.utils import get_user_carts


class CartMixin:
    def get_cart(self, request, product=None, cart_id=None, variant=None):
        if request.user.is_authenticated:
            query_kwargs = {"user": request.user}
        else:
            query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product
        elif cart_id:
            query_kwargs["id"] = cart_id

        return Cart.objects.filter(**query_kwargs).first()

    def render_cart(self, request):
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        referer = request.headers.get("referer")
        if reverse("orders:create") in referer:
            context["order"] = True

        return render_to_string(
            "carts/includes/included_cart.html",
            {"carts": user_cart},
            request=request,
        )
