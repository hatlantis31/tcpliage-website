# metal_designer/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'materials', views.MaterialViewSet)
router.register(r'shape-templates', views.ShapeTemplateViewSet)
router.register(r'coatings', views.CoatingViewSet)
router.register(r'colors', views.ColorViewSet)
router.register(r'metal-designs', views.MetalDesignViewSet,
                basename='metal-designs')

urlpatterns = [
    path('', include(router.urls)),
]
