from django.urls import path

from gearcore.main import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
]
