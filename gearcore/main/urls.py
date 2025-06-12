from django.urls import path

from gearcore.main import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
