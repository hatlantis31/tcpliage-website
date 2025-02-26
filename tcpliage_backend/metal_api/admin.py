# admin.py
from django.contrib import admin
from .models import MetalDesign, PriceQuote


@admin.register(MetalDesign)
class MetalDesignAdmin(admin.ModelAdmin):
    list_display = ('name', 'material', 'shape',
                    'created_at', 'status', 'price')
    list_filter = ('status', 'material', 'finish')
    search_fields = ('name', 'notes', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'name', 'user', 'email', 'created_at', 'updated_at', 'status')
        }),
        ('Specifications', {
            'fields': ('width', 'height', 'depth', 'material', 'thickness', 'finish', 'shape')
        }),
        ('Design Details', {
            'fields': ('custom_path', 'features_json', 'notes', 'svg_preview')
        }),
        ('Pricing', {
            'fields': ('price', 'quote_notes', 'quoted_at', 'quoted_by')
        }),
    )


@admin.register(PriceQuote)
class PriceQuoteAdmin(admin.ModelAdmin):
    list_display = ('design', 'price', 'created_at',
                    'estimated_production_days', 'is_current')
    list_filter = ('is_current', 'created_at')
    search_fields = ('design__name', 'notes')
    readonly_fields = ('created_at',)
