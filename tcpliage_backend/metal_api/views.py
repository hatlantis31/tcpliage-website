from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MetalPiece, Order
from .serializers import MetalPieceSerializer, OrderSerializer

class MetalPieceViewSet(viewsets.ModelViewSet):
    queryset = MetalPiece.objects.all()
    serializer_class = MetalPieceSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# metal_api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import math

def calculate_angle(p1, p2, p3):
    """Calcule l'angle entre trois points en degrés"""
    a = math.sqrt((p2['x'] - p1['x'])**2 + (p2['y'] - p1['y'])**2)
    b = math.sqrt((p2['x'] - p3['x'])**2 + (p2['y'] - p3['y'])**2)
    c = math.sqrt((p3['x'] - p1['x'])**2 + (p3['y'] - p1['y'])**2)

    cos_angle = (a**2 + b**2 - c**2) / (2 * a * b)
    angle = math.degrees(math.acos(max(-1, min(1, cos_angle))))
    return angle

@api_view(['POST'])
def validate_piece(request):
    points = request.data.get('points', [])
    thickness = request.data.get('thickness')
    material = request.data.get('material')

    # Validation minimale
    if len(points) < 3:
        return Response({
            'valid': False,
            'message': "La pièce doit avoir au moins 3 points"
        })

    # Vérifier l'épaisseur
    if thickness < 0.5 or thickness > 50:
        return Response({
            'valid': False,
            'message': "L'épaisseur doit être entre 0.5mm et 50mm"
        })

    # Vérifier les dimensions maximales
    max_x = max(p['x'] for p in points)
    max_y = max(p['y'] for p in points)
    if max_x > 3000 or max_y > 3000:
        return Response({
            'valid': False,
            'message': "Les dimensions ne peuvent pas dépasser 3000mm"
        })

    # Vérifier les angles minimaux
    min_angle = 30
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        p3 = points[(i + 2) % len(points)]

        angle = calculate_angle(p1, p2, p3)
        if angle < min_angle:
            return Response({
                'valid': False,
                'message': f"L'angle au point {i+2} est trop aigu (minimum {min_angle}°)"
            })

    return Response({
        'valid': True,
        'message': "OK"
    })
