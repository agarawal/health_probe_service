# health_probe/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('probe/', views.get_probe, name='get_probe'),
    path('probe/create/', views.create_probe, name='create_probe'),
    path('probe/delete/', views.delete_probe, name='delete_probe'),
]