from django.contrib import admin
from app.properties.models import Property, Phase, Plot


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'property_type', 'price', 'phase_number', 'created_at', 'updated_at', 'created_by', 'director',
        'current_lead')
    search_fields = ('name', 'location', 'created_by__username', 'director__username', 'current_lead__name')
    list_filter = ('property_type', 'created_at')


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('property', 'phase_number', 'start_date', 'estimated_completion_date', 'status')
    search_fields = ('property__name', 'description')
    list_filter = ('status', 'start_date')


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = (
        'phase', 'plot_number', 'dimensions', 'facing', 'soil_type', 'plantation', 'price', 'availability',
        'created_at',
        'updated_at')
    search_fields = ('plot_number', 'phase__property__name')
    list_filter = ('availability', 'facing', 'soil_type', 'created_at')
