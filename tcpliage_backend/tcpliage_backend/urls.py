<<<<<<< HEAD
# urls.py
=======
# tcpliage_backend/urls.py (Project-level URLs)
from django.contrib import admin
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
from django.urls import path, include
from rest_framework.routers import DefaultRouter
<<<<<<< HEAD
from metal_api import views
=======
from metal_api.views import (
    ServiceViewSet, 
    MetalPieceViewSet, 
    OrderViewSet,
    get_shapes,
    get_shape_config,
    validate_design,
    save_design,
    get_design
)
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9

# Create a router and register viewsets
router = DefaultRouter()
<<<<<<< HEAD
router.register(r'designs', views.MetalDesignViewSet)
router.register(r'quotes', views.PriceQuoteViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Add additional endpoints if needed
]
=======
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'pieces', MetalPieceViewSet, basename='piece')
router.register(r'orders', OrderViewSet, basename='order')

# API URL patterns
api_patterns = [
    # ViewSet URLs
    path('', include(router.urls)),
    
    # Shape-related endpoints
    path('shapes/', get_shapes, name='shapes-list'),
    path('shapes/<str:shape_id>/config/', get_shape_config, name='shape-config'),
    
    # Design-related endpoints
    path('designs/', save_design, name='save-design'),
    path('designs/<int:design_id>/', get_design, name='get-design'),
    path('validate-design/', validate_design, name='validate-design'),
]

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include((api_patterns, 'api'), namespace='api')),
    
    # Auth endpoints (if using DRF auth)
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar URLs (only in debug mode)
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
