# tcpliage_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from metal_api.views import MetalPieceViewSet, OrderViewSet, ServiceViewSet, validate_piece

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'pieces', MetalPieceViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/validate-piece/', validate_piece),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
