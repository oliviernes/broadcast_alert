"""Map URL patterns to view function"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.search, name="welcome"),
    path("my_results/<int:my_search_id>", views.my_results, name="my_results"),
    path("my_search/", views.my_search, name="my_search"),
    path('delete/<int:pk>', views.delete, name="delete"),
]
