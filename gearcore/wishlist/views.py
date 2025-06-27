import json

from django.http import JsonResponse
from django.views import View

from gearcore.goods.models import Motorcycle
from gearcore.wishlist.models import Wishlist, WishlistItem


class WishlistAddView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        slug = data.get('productSlug', '')

        if not slug:
            return JsonResponse({'status': '400', 'debug_message': "потрібен slug продукту", 'html': None, })

        user = request.user

        wishlist, _ = Wishlist.objects.get_or_create(user=user)

        try:
            motorcycle = Motorcycle.objects.get(slug=slug)
        except Motorcycle.DoesNotExist:
            return JsonResponse({'status': '400', 'debug_message': "такий товар не знайдено", 'html': None, })

        WishlistItem.objects.get_or_create(wishlist=wishlist, product=motorcycle)

        return JsonResponse({'status': '200', 'debug_message': "товар додано до обраних", 'html': None, })

wishlist_add_view = WishlistAddView.as_view()
