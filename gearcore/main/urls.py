from django.urls import path

from gearcore.main import views
from gearcore.main.views import (index_view, about_view)

app_name = "main"
urlpatterns = [
    path("", view=index_view, name="index"),
    path("about/", view=about_view, name="about"),
    path("contact/", views.contact, name="contact"),
]
