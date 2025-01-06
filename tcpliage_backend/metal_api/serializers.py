from rest_framework import serializers
from .models import MetalPiece, Order

class MetalPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalPiece
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
