from django.urls import path

from gearcore.wishlist.views import wishlist_add_view
from gearcore.wishlist.views import wishlist_remove_view

app_name = "wishlist"

urlpatterns = [
    path("add/", view=wishlist_add_view, name="add"),
    path("remove/", view=wishlist_remove_view, name="remove"),
]
