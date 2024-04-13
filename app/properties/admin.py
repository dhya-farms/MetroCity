from django.contrib import admin
from app.properties.models import Property, Phase, Plot, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Specifies the number of empty forms to display
    fields = ['image']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'property_type', 'price', 'location', 'created_at', 'updated_at']
    list_filter = ['property_type', 'area_of_purpose', 'created_at', 'updated_at', 'price']
    search_fields = ['name', 'description', 'location', 'details']
    inlines = [PropertyImageInline]
    readonly_fields = ['created_at', 'updated_at']  # Fields that should be read-only in the admin interface
    fieldsets = (
        (None, {'fields': ('name', 'description', 'details', 'price')}),
        ('Location Details', {'fields': ('location', 'gmap_url')}),
        ('Classification', {'fields': ('property_type', 'area_of_purpose')}),
        ('Administrative', {'fields': ('created_by', 'director', 'current_lead', 'created_at', 'updated_at')}),
    )


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'phase_number', 'start_date', 'estimated_completion_date', 'status')
    search_fields = ('property__name', 'description')
    list_filter = ('status', 'start_date')


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'phase', 'plot_number', 'dimensions', 'facing', 'soil_type', 'plantation', 'price', 'availability',
        'created_at',
        'updated_at')
    search_fields = ('plot_number', 'phase__property__name')
    list_filter = ('availability', 'facing', 'soil_type', 'created_at')
