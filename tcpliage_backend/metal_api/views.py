# views.py
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Service, MetalPiece, Order
from .serializers import ServiceSerializer, MetalPieceSerializer, OrderSerializer
import math
from django.http import JsonResponse


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class MetalPieceViewSet(viewsets.ModelViewSet):
    queryset = MetalPiece.objects.all()
    serializer_class = MetalPieceSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
#########################################################################
######### metal_api/views.py        ###################################
#########################################################################


SHAPES = {
    'rectangle': {
        'id': 'rectangle',
        'name': 'Rectangle',
        'preview_url': '/static/shapes/rectangle.svg',
        'dimensions': {
            'length': {'label': 'Longueur', 'min': 10, 'max': 1000, 'step': 1},
            'width': {'label': 'Largeur', 'min': 10, 'max': 1000, 'step': 1}
        }
    },
    'circle': {
        'id': 'circle',
        'name': 'Cercle',
        'preview_url': '/static/shapes/circle.svg',
        'dimensions': {
            'diameter': {'label': 'Diamètre', 'min': 10, 'max': 1000, 'step': 1}
        }
    }
}


@api_view(['GET'])
def get_shapes(request):
    return Response(list(SHAPES.values()))


@api_view(['GET'])
def get_shape_config(request, shape_id):
    if shape_id not in SHAPES:
        return Response({'error': 'Shape not found'}, status=404)
    return Response(SHAPES[shape_id])


@api_view(['POST'])
def validate_design(request):
    design = request.data

    # Validate material
    if design['material'] not in ['acier', 'aluminium', 'inox']:
        return Response({
            'valid': False,
            'message': 'Matériau invalide'
        })

    # Validate shape
    if design['shape'] not in SHAPES:
        return Response({
            'valid': False,
            'message': 'Forme invalide'
        })

    # Validate dimensions
    shape_config = SHAPES[design['shape']]
    for key, config in shape_config['dimensions'].items():
        value = float(design['dimensions'].get(key, 0))
        if value < config['min'] or value > config['max']:
            return Response({
                'valid': False,
                'message': f'Dimension {config["label"]} invalide'
            })

    # Calculate price
    price = calculate_price(design)

    return Response({
        'valid': True,
        'message': 'Design validé',
        'price': price
    })


def calculate_price(design):
    # Basic price calculation
    base_prices = {
        'acier': 1.0,
        'aluminium': 1.5,
        'inox': 2.0
    }

    # Calculate area based on shape
    area = 0
    if design['shape'] == 'rectangle':
        area = float(design['dimensions']['length']) * \
            float(design['dimensions']['width'])
    elif design['shape'] == 'circle':
        diameter = float(design['dimensions']['diameter'])
        area = 3.14159 * (diameter/2) ** 2

    return round(area * base_prices[design['material']] / 100, 2)
