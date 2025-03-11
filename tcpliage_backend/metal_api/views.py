# metal_designer/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone

from .models import Material, ShapeTemplate, Coating, Color, MetalDesign
from .serializers import (
    MaterialSerializer, ShapeTemplateSerializer, CoatingSerializer,
    ColorSerializer, MetalDesignCreateSerializer, MetalDesignDetailSerializer
)


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing materials."""
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class ShapeTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing shape templates."""
    queryset = ShapeTemplate.objects.all()
    serializer_class = ShapeTemplateSerializer


class CoatingViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing coatings."""
    queryset = Coating.objects.all()
    serializer_class = CoatingSerializer

    @action(detail=False, methods=['get'])
    def for_material(self, request):
        """List coatings compatible with a specific material."""
        material_id = request.query_params.get('material_id')
        if not material_id:
            return Response(
                {"error": "Material ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        coatings = Coating.objects.filter(compatible_materials__id=material_id)
        serializer = self.get_serializer(coatings, many=True)
        return Response(serializer.data)


class ColorViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing colors."""
    queryset = Color.objects.all()
    serializer_class = ColorSerializer


class MetalDesignViewSet(viewsets.ModelViewSet):
    """API endpoint for creating and managing metal designs."""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Limit designs to the current user if authenticated."""
        user = self.request.user
        if user.is_authenticated:
            return MetalDesign.objects.filter(user=user)
        return MetalDesign.objects.none()

    def get_serializer_class(self):
        """Use different serializers for create and retrieve operations."""
        if self.action == 'create':
            return MetalDesignCreateSerializer
        return MetalDesignDetailSerializer

    def perform_create(self, serializer):
        """Set the user on design creation if authenticated."""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()
