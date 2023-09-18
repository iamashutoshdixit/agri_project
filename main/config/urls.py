# django imports
from django.urls import path

# app imports
from . import views

urlpatterns = [
    path("", views.get_config),
]
