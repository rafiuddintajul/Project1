from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.wiki, name="search"),
    path("search/<str:title>", views.wiki),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:title>", views.edit, name="edit_url"),
    path("random", views.random_entry, name="random_entry")
]
