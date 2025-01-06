from django.db import models

class MetalPiece(models.Model):
    MATERIAL_CHOICES = [
        ('acier', 'Acier'),
        ('aluminium', 'Aluminium'),
        ('inox', 'Inox'),
    ]

    points = models.JSONField()  # Store points as JSON
    thickness = models.FloatField()
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.material} piece - {self.created_at}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
    ]

    metal_piece = models.ForeignKey(MetalPiece, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
