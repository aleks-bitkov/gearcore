from django.urls import path

from gearcore.carts import views

app_name = "carts"

urlpatterns = [
    path("add/", views.cart_add_view, name="add" ),
    path("change/", views.cart_change_view, name="change" ),
    path("remove/", views.cart_remove_view, name="remove" ),
]
