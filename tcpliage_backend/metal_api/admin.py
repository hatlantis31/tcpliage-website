# admin.py
from django.contrib import admin
from .models import Service, ServiceCharacteristic, MetalPiece, Order


class ServiceCharacteristicInline(admin.TabularInline):
    model = ServiceCharacteristic
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description')
    search_fields = ('titre', 'description')
    inlines = [ServiceCharacteristicInline]


@admin.register(MetalPiece)
class MetalPieceAdmin(admin.ModelAdmin):
    list_display = ('material', 'thickness', 'created_at')
    list_filter = ('material', 'created_at')
    search_fields = ('material',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client_name', 'client_email')
