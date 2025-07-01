from django.urls import path

from gearcore.goods.views import product_view, catalog_view, product_color_change_view

app_name = "goods"

urlpatterns = [
    path("", view=catalog_view, name="catalog"),
    path("search/", view=catalog_view, name="search"),
    path("product/<slug:slug>", view=product_view, name="product"),
    # path("product/<slug:slug>/color/<slug:color-slug>", view=product_color_change_view, name="product_color"),
]
