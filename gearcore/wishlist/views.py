import json

from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from gearcore.goods.models import MotorcycleVariant
from gearcore.wishlist.models import Wishlist
from gearcore.wishlist.models import WishlistItem


class WishlistAddView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        variant_id = data.get("variantId", "")
        if not variant_id:
            return JsonResponse(
                {
                    "debug_message": "потрібен id варіанту продукту",
                    "html": None,
                },
                status=400,
            )

        user = request.user

        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        try:
            variant = MotorcycleVariant.objects.get(id=variant_id)
        except MotorcycleVariant.DoesNotExist:
            return JsonResponse(
                {
                    "status": "400",
                    "debug_message": "такий варіант товар не знайдено",
                    "html": None,
                },
            )

        WishlistItem.objects.get_or_create(wishlist=wishlist, variant=variant)

        return JsonResponse(
            {
                "debug_message": "товар додано до обраних",
                "action": reverse("wishlist:remove"),
            },
            status=200,
        )


wishlist_add_view = WishlistAddView.as_view()


class WishlistRemoveView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        variant_id = data.get("variantId", "")

        if not variant_id:
            return JsonResponse(
                {"debug_message": "потрібен id варіант продукту", "html": None},
                status=400,
            )

        user = request.user

        try:
            wishlist = Wishlist.objects.get(user=user)
        except Wishlist.DoesNotExist:
            return JsonResponse(
                {"debug_message": "не знайдено улюбленого списку для користувача ", "html": None},
                status=400,
            )

        try:
            variant = MotorcycleVariant.objects.get(id=variant_id)
        except MotorcycleVariant.DoesNotExist:
            return JsonResponse(
                {"debug_message": f"не знайдено товару за id '{variant_id}'", "html": None},
                status=400,
            )

        try:
            wishlist_item = WishlistItem.objects.get(
                wishlist=wishlist,
                variant=variant,
            )
            wishlist_item.delete()
        except WishlistItem.DoesNotExist:
            ...

        return JsonResponse(
            {
                "debug_message": "товар було прибрано з обраних",
                "action": reverse("wishlist:add"),
            },
            status=200,
        )


wishlist_remove_view = WishlistRemoveView.as_view()
