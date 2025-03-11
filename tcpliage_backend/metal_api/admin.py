# metal_designer/admin.py
from django.contrib import admin
from .models import Material, ShapeTemplate, Coating, Color, MetalDesign


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'density', 'price_per_kg')
    search_fields = ('name', 'description')


@admin.register(ShapeTemplate)
class ShapeTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'description')


@admin.register(Coating)
class CoatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price_factor')
    search_fields = ('name', 'description')
    filter_horizontal = ('compatible_materials',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hex_code')
    search_fields = ('name',)


@admin.register(MetalDesign)
class MetalDesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'material', 'status',
                    'created_at', 'quoted_price')
    list_filter = ('status', 'material', 'coating')
    search_fields = ('id', 'user__username', 'notes')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'status', 'created_at', 'updated_at', 'notes')
        }),
        ('Design Specifications', {
            'fields': ('material', 'shape_template', 'shape_dimensions', 'cutouts', 'coating', 'color')
        }),
        ('Quote Information', {
            'fields': ('quoted_price', 'quoted_at', 'estimated_production_time')
        }),
    )
