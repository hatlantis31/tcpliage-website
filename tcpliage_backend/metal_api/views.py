# views.py
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import MetalDesign, PriceQuote
from .serializers import MetalDesignSerializer, PriceQuoteSerializer


class MetalDesignViewSet(viewsets.ModelViewSet):
    queryset = MetalDesign.objects.all()
    serializer_class = MetalDesignSerializer

    def get_queryset(self):
        user = self.request.user
        # If staff, show all designs. Otherwise, only show the user's designs
        if user.is_authenticated:
            if user.is_staff:
                return MetalDesign.objects.all()
            return MetalDesign.objects.filter(user=user)
        return MetalDesign.objects.none()

    def create(self, request, *args, **kwargs):
        # Add user if authenticated
        if request.user.is_authenticated:
            request.data['user'] = request.user.id

        # Process dimensions from frontend format
        if 'dimensions' in request.data:
            dimensions = request.data.pop('dimensions')
            request.data['width'] = dimensions.get('width', 0)
            request.data['height'] = dimensions.get('height', 0)
            request.data['depth'] = dimensions.get('depth', 0)

        # Process material from frontend format
        if 'material' in request.data and isinstance(request.data['material'], dict):
            material_data = request.data.pop('material')
            request.data['material'] = material_data.get('type', 'steel')
            request.data['thickness'] = material_data.get('thickness', 1.0)
            request.data['finish'] = material_data.get('finish', 'none')

        # Create a name if not provided
        if not request.data.get('name'):
            material = request.data.get('material', 'metal')
            shape = request.data.get('shape', 'piece')
            timestamp = timezone.now().strftime("%Y%m%d-%H%M")
            request.data['name'] = f"{material} {shape} {timestamp}"

        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, permissions.IsAdminUser])
    def add_quote(self, request, pk=None):
        design = self.get_object()

        serializer = PriceQuoteSerializer(data=request.data)
        if serializer.is_valid():
            # Mark previous quotes as not current
            design.quotes.update(is_current=False)

            # Create new quote
            quote = serializer.save(
                design=design,
                created_by=request.user,
                is_current=True
            )

            # Update design with quote information
            design.status = 'quoted'
            design.price = quote.price
            design.quote_notes = quote.notes
            design.quoted_at = timezone.now()
            design.quoted_by = request.user
            design.save()

            # Notify customer
            if design.user and design.user.email:
                send_mail(
                    'Price Quote for Your Metal Design',
                    f'Your design "{design.name}" has been quoted at ${quote.price}. Log in to view details.',
                    settings.DEFAULT_FROM_EMAIL,
                    [design.user.email],
                    fail_silently=True,
                )
            elif design.email:
                send_mail(
                    'Price Quote for Your Metal Design',
                    f'Your design has been quoted at ${quote.price}. Please check your account for details.',
                    settings.DEFAULT_FROM_EMAIL,
                    [design.email],
                    fail_silently=True,
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def accept_quote(self, request, pk=None):
        design = self.get_object()

        if design.status != 'quoted':
            return Response(
                {"detail": "This design does not have an active quote to accept."},
                status=status.HTTP_400_BAD_REQUEST
            )

        design.status = 'accepted'
        design.save()

        return Response({"status": "quote accepted"})

    @action(detail=True, methods=['post'])
    def reject_quote(self, request, pk=None):
        design = self.get_object()

        if design.status != 'quoted':
            return Response(
                {"detail": "This design does not have an active quote to reject."},
                status=status.HTTP_400_BAD_REQUEST
            )

        design.status = 'rejected'
        design.save()

        return Response({"status": "quote rejected"})


class PriceQuoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceQuote.objects.all()
    serializer_class = PriceQuoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PriceQuote.objects.all()
        return PriceQuote.objects.filter(design__user=user)
