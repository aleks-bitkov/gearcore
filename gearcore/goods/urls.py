from django.urls import path

from gearcore.goods import views

app_name = "goods"

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("search/", views.catalog, name="search"),
    path("product/<slug:slug>", views.product, name="product"),
]
