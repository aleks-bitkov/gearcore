from django.contrib import admin

from gearcore.wishlist.models import Wishlist, WishlistItem

admin.site.register(Wishlist)
admin.site.register(WishlistItem)
