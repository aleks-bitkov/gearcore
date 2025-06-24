from django.urls import path
from gearcore.orders import views

app_name = "orders"

urlpatterns = [
    path("create", views.create_oreder_view, name="create")
]
