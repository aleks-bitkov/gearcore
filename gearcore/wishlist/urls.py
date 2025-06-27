from django.urls import path

app_name = "wishlist"

from .views import wishlist_add_view
urlpatterns = [
    path("add/", view=wishlist_add_view, name="add"),
]
