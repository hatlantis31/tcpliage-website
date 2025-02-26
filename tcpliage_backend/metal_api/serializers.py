# serializers.py
from rest_framework import serializers
from .models import MetalDesign, PriceQuote


class MetalDesignSerializer(serializers.ModelSerializer):
    features = serializers.JSONField(required=False)

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


class PriceQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceQuote
        fields = ['id', 'design', 'created_at', 'price',
                  'estimated_production_days', 'notes', 'is_current']
        read_only_fields = ['id', 'created_at']
