from django.urls import path

from .views import user_cart
from .views import user_orders
from .views import user_profile_view
from .views import user_redirect_view
from .views import user_wishlist_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("profile/", view=user_profile_view, name="detail"),
    path("cart/", view=user_cart, name="cart"),
    path("wishlist/", view=user_wishlist_view, name="wishlist"),
    path("orders/", view=user_orders, name="orders"),
]
