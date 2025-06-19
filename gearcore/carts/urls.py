from django.urls import path

from gearcore.carts import views

app_name = "carts"

urlpatterns = [
    path("add/<slug:slug>", views.cart_add, name="add" ),
    path("change/<slug:slug>", views.cart_change, name="change" ),
    path("remove/<slug:slug>", views.cart_remove, name="remove" ),
]
