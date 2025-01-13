# serializers.py
from rest_framework import serializers
from .models import Service, ServiceCharacteristic, MetalPiece, Order, Design

class ServiceCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCharacteristic
        fields = ['description']

class ServiceSerializer(serializers.ModelSerializer):
    caracteristiques = ServiceCharacteristicSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'titre', 'description', 'image', 'caracteristiques']

class MetalPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalPiece
        fields = '__all__'

class DesignPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalPiece
        fields = ['piece_id', 'material', 'shape', 'dimensions', 
                 'position_x', 'position_y', 'thickness', 'created_at']

class DesignSerializer(serializers.ModelSerializer):
    pieces = DesignPieceSerializer(many=True, read_only=True)

    class Meta:
        model = Design
        fields = ['id', 'name', 'pieces', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    design = DesignSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
