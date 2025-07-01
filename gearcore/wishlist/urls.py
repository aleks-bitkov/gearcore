from django.urls import path

app_name = "wishlist"

from gearcore.wishlist.views import wishlist_add_view, wishlist_remove_view
urlpatterns = [
    path("add/", view=wishlist_add_view, name="add"),
    path("remove/", view=wishlist_remove_view, name="remove"),
]
