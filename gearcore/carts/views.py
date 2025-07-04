import json

from django.http import JsonResponse
from django.views import View

from gearcore.carts.mixins import CartMixin
from gearcore.carts.models import Cart
from gearcore.goods.models import Motorcycle
from gearcore.goods.models import MotorcycleVariant


class CartAddView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slug = data.get("slug", None)
        variant_id = data.get("variant_id", None)

        product = Motorcycle.objects.get(slug=slug)
        variant = MotorcycleVariant.objects.get(id=variant_id)

        cart = self.get_cart(request, product=product, variant=variant)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key if not request.user.is_authenticated else "None",
                product=product,
                variant=variant,
                quantity=1,
            )

        response_data = {
            "status": 200,
            "debug_message": "успішно додано до кошику",
            "html": self.render_cart(request),
        }

        return JsonResponse(response_data)


cart_add_view = CartAddView.as_view()


class CartChangeView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        action = data.get("action", None)
        cart_id = data.get("id_cart", None)

        cart = self.get_cart(request, cart_id=cart_id)

        if action == "increment":
            cart.quantity += 1
            cart.save()
        elif action == "decrement":
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
            else:
                cart.delete()

        return JsonResponse(
            {
                "status": 200,
                "debug_message": "успішно оновлено кількість",
                "html": self.render_cart(request),
            },
        )


cart_change_view = CartChangeView.as_view()


class CartRemoveView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        cart_id = data.get("id_cart", None)

        cart = self.get_cart(request, cart_id=cart_id)
        cart.delete()

        return JsonResponse(
            {
                "status": 200,
                "debug_message": "успішно видалено кошик",
                "html": self.render_cart(request),
            },
        )


cart_remove_view = CartRemoveView.as_view()
