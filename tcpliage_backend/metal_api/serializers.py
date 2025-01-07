# serializers.py
from rest_framework import serializers
from .models import Service, ServiceCharacteristic, MetalPiece, Order


class ServiceCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCharacteristic
        fields = ['description']


class ServiceSerializer(serializers.ModelSerializer):
    caracteristiques = ServiceCharacteristicSerializer(
        many=True, read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'titre', 'description', 'image', 'caracteristiques']


class MetalPieceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetalPiece
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
