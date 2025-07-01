from django.contrib import admin

from gearcore.wishlist.models import Wishlist
from gearcore.wishlist.models import WishlistItem

admin.site.register(Wishlist)
admin.site.register(WishlistItem)
