from django.urls import path

from gearcore.carts import views

app_name = "carts"

urlpatterns = [
    path("add/<int:pk>", views.cart_add, name="add" ),
    path("change", views.cart_change, name="change" ),
    path("remove", views.cart_remove, name="remove" ),
]
