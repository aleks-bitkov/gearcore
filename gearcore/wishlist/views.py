import json

from django.http import JsonResponse
from django.urls import reverse
from django.views import View

from gearcore.goods.models import Motorcycle
from gearcore.wishlist.models import Wishlist
from gearcore.wishlist.models import WishlistItem


class WishlistAddView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slug = data.get("productSlug", "")

        if not slug:
            return JsonResponse(
                {
                    "status": "400",
                    "debug_message": "потрібен slug продукту",
                    "html": None,
                },
            )

        user = request.user

        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        try:
            motorcycle = Motorcycle.objects.get(slug=slug)
        except Motorcycle.DoesNotExist:
            return JsonResponse(
                {
                    "status": "400",
                    "debug_message": "такий товар не знайдено",
                    "html": None,
                },
            )

        WishlistItem.objects.get_or_create(wishlist=wishlist, product=motorcycle)

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
        slug = data.get("productSlug", "")

        if not slug:
            return JsonResponse(
                {"debug_message": "потрібен slug продукту", "html": None}, status=400,
            )

        user = request.user

        try:
            wishlist = Wishlist.objects.get(user=user)
        except Wishlist.DoesNotExist:
            return JsonResponse(
                {"debug_message": "не знайдено списку для користувача ", "html": None},
                status=400,
            )

        try:
            motorcycle = Motorcycle.objects.get(slug=slug)
        except Motorcycle.DoesNotExist:
            return JsonResponse(
                {"debug_message": f"не знайдено товару за slug '{slug}'", "html": None},
                status=400,
            )

        try:
            wishlist_item = WishlistItem.objects.get(
                wishlist=wishlist, product=motorcycle,
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
