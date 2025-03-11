# metal_designer/models.py
from django.db import models
from django.contrib.auth import get_user_model
import uuid
import json

User = get_user_model()


class Material(models.Model):
    """Model for metal materials."""
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    density = models.FloatField(help_text="Density in g/cm³")
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='materials/', null=True, blank=True)

    def __str__(self):
        return self.name


class ShapeTemplate(models.Model):
    """Model for predefined shapes."""
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    svg_path = models.TextField(help_text="SVG path data for rendering")

    def __str__(self):
        return self.name


class Coating(models.Model):
    """Model for coating options."""
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_factor = models.FloatField(help_text="Multiplier for the base price")
    image = models.ImageField(upload_to='coatings/', null=True, blank=True)

    # Many-to-many relationship with materials
    compatible_materials = models.ManyToManyField(Material)

    def __str__(self):
        return self.name


class Color(models.Model):
    """Model for coating colors."""
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    hex_code = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class MetalDesign(models.Model):
    """Model for user metal piece designs."""
    STATUS_CHOICES = [
        ('pending', 'Pending Quote'),
        ('quoted', 'Quote Provided'),
        ('accepted', 'Quote Accepted'),
        ('rejected', 'Quote Rejected'),
        ('in_production', 'In Production'),
        ('completed', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    # Design specifications
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    shape_template = models.ForeignKey(ShapeTemplate, on_delete=models.PROTECT)
    shape_dimensions = models.JSONField(
        help_text="JSON object with dimensions")
    cutouts = models.JSONField(
        default=list, help_text="JSON array of cutout coordinates")
    coating = models.ForeignKey(
        Coating, on_delete=models.PROTECT, null=True, blank=True)
    color = models.ForeignKey(
        Color, on_delete=models.PROTECT, null=True, blank=True)

    # Quote information
    quoted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    quoted_at = models.DateTimeField(null=True, blank=True)
    estimated_production_time = models.PositiveIntegerField(
        null=True, blank=True, help_text="Estimated production time in days")

    # Additional metadata
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Design {self.id} - {self.status}"

    @property
    def get_dimensions_display(self):
        """Format dimensions for display."""
        dimensions = self.shape_dimensions
        if self.shape_template.id == 'circle':
            return f"Diameter: {dimensions.get('diameter')}mm, Thickness: {dimensions.get('thickness')}mm"
        return f"Width: {dimensions.get('width')}mm, Height: {dimensions.get('height')}mm, Thickness: {dimensions.get('thickness')}mm"

    @property
    def cutout_count(self):
        """Return the number of cutouts."""
        return len(self.cutouts) if self.cutouts else 0
