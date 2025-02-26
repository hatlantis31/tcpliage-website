# serializers.py
from rest_framework import serializers
<<<<<<< HEAD
from .models import MetalDesign, PriceQuote


class MetalDesignSerializer(serializers.ModelSerializer):
    features = serializers.JSONField(required=False)
=======
from .models import Service, ServiceCharacteristic, MetalPiece, Order, Design

class ServiceCharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCharacteristic
        fields = ['description']

class ServiceSerializer(serializers.ModelSerializer):
    caracteristiques = ServiceCharacteristicSerializer(many=True, read_only=True)
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9

    class Meta:
        model = MetalDesign
        fields = [
            'id', 'name', 'created_at', 'updated_at',
            'width', 'height', 'depth',
            'material', 'thickness', 'finish',
            'shape', 'custom_path', 'features',
            'notes', 'svg_preview', 'status',
            'price', 'quote_notes', 'quoted_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at',
                            'status', 'price', 'quote_notes', 'quoted_at']

    def create(self, validated_data):
        features_data = validated_data.pop('features', None)
        design = MetalDesign.objects.create(**validated_data)

        if features_data:
            design.features = features_data
            design.save()

        return design

    def update(self, instance, validated_data):
        if 'features' in validated_data:
            instance.features = validated_data.pop('features')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

<<<<<<< HEAD

class PriceQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceQuote
        fields = ['id', 'design', 'created_at', 'price',
                  'estimated_production_days', 'notes', 'is_current']
        read_only_fields = ['id', 'created_at']
=======
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
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
