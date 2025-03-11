# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from metal_api import views

# Create a router and register viewsets

urlpatterns = [
    path('api/', include('metal_api.urls')),
    # Add additional endpoints if needed
]
