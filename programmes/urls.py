"""Map URL patterns to view function"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name="welcome"),
    path('results/', views.search, name="results"),
    path('my_search/', views.my_search, name="my_search"),
]
