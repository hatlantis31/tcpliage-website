# models.py
from django.db import models
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
    )
    description = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Caractéristique'
        verbose_name_plural = 'Caractéristiques'

    def __str__(self):
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

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]

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
