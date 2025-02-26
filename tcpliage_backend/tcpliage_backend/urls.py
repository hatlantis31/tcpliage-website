# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from metal_api import views

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'designs', views.MetalDesignViewSet)
router.register(r'quotes', views.PriceQuoteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Add additional endpoints if needed
]
