# models.py
from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import User
import uuid
import json


class MetalDesign(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('quoted', 'Price Quoted'),
        ('accepted', 'Quote Accepted'),
        ('rejected', 'Quote Rejected'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
=======
from .constants import MATERIALS, SHAPES
import uuid


def generate_uuid():
    """Generate a unique UUID string"""
    return str(uuid.uuid4())

class Service(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.titre

class ServiceCharacteristic(models.Model):
    service = models.ForeignKey(
        Service,
        related_name='caracteristiques',
        on_delete=models.CASCADE
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
    )

<<<<<<< HEAD
    MATERIAL_CHOICES = (
        ('steel', 'Steel'),
        ('aluminum', 'Aluminum'),
        ('copper', 'Copper'),
        ('brass', 'Brass'),
    )

    FINISH_CHOICES = (
        ('none', 'None (Raw)'),
        ('polished', 'Polished'),
        ('brushed', 'Brushed'),
        ('painted', 'Painted'),
        ('powder-coated', 'Powder Coated'),
    )

    # Identification
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # User information
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(blank=True)  # For non-registered users

    # Status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # Dimensions
    width = models.FloatField()
    height = models.FloatField()
    depth = models.FloatField()

    # Material
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    thickness = models.FloatField()
    finish = models.CharField(max_length=20, choices=FINISH_CHOICES)

    # Shape and features
    shape = models.CharField(max_length=20)
    custom_path = models.TextField(blank=True)
    features_json = models.TextField(blank=True)  # Stored as JSON

    # Additional info
    notes = models.TextField(blank=True)
    svg_preview = models.TextField(blank=True)  # Store SVG as text

    # Price quote
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    quote_notes = models.TextField(blank=True)
    quoted_at = models.DateTimeField(null=True, blank=True)
    quoted_by = models.ForeignKey(
        User, related_name='quoted_designs', on_delete=models.SET_NULL, null=True, blank=True)

=======
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
<<<<<<< HEAD
        return f"{self.name or 'Unnamed design'} ({self.id})"
=======
        return f"{self.service.titre} - {self.description[:30]}"

class MetalPiece(models.Model):
    MATERIAL_CHOICES = [(k, v['name']) for k, v in MATERIALS.items()]
    SHAPE_CHOICES = [(k, v['name']) for k, v in SHAPES.items()]

    piece_id = models.CharField(
        max_length=36, 
        unique=True,
        default=generate_uuid  # Use the function name without ()
    )
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    shape = models.CharField(max_length=20, choices=SHAPE_CHOICES)
    dimensions = models.JSONField(default=dict)
    position_x = models.FloatField(default=0)
    position_y = models.FloatField(default=0)
    thickness = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.material} {self.shape} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.piece_id:
            self.piece_id = generate_uuid()
        super().save(*args, **kwargs)

class Design(models.Model):
    name = models.CharField(max_length=100, default='Untitled Design')
    pieces = models.ManyToManyField(MetalPiece, related_name='designs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Design {self.id} - {self.name}"
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9

    @property
    def features(self):
        if not self.features_json:
            return []
        return json.loads(self.features_json)

<<<<<<< HEAD
    @features.setter
    def features(self, features_list):
        self.features_json = json.dumps(features_list)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('design_detail', args=[str(self.id)])


class PriceQuote(models.Model):
    design = models.ForeignKey(
        MetalDesign, on_delete=models.CASCADE, related_name='quotes')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_production_days = models.IntegerField(default=7)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return f"Quote ${self.price} for {self.design}"
=======
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.client_name}"
>>>>>>> c12881765c31cf1adc41de23ea8096dac86cd4c9
