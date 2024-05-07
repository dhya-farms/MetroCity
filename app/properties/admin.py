from django.contrib import admin
from app.properties.models import Property, Phase, Plot, PropertyImage

from django.contrib import admin
from .models import PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Specifies the number of empty forms to display
    fields = ['image', 'is_slider_image', 'slider_image_order']


class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 1


class PlotInline(admin.TabularInline):
    model = Plot
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'property_type', 'location', 'created_at', 'updated_at']
    list_filter = ['property_type', 'area_of_purpose', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'location', 'details']
    inlines = [PropertyImageInline, PhaseInline]
    readonly_fields = ['created_at', 'updated_at']  # Fields that should be read-only in the admin interface
    fieldsets = (
        (None, {'fields': ('name', 'description', 'details')}),
        ('Location Details', {'fields': ('location', 'gmap_url')}),
        ('Classification', {'fields': ('property_type', 'area_of_purpose')}),
        ('Administrative', {'fields': ('created_by', 'director', 'current_lead', 'created_at', 'updated_at')}),
    )


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'property', 'phase_number', 'status']
    inlines = [PlotInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super(PhaseAdmin, self).get_inline_instances(request, obj)


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'phase', 'plot_number', 'dimensions', 'is_sold']
    list_filter = ['is_sold', 'phase', 'availability']
    search_fields = ['plot_number']

    def get_form(self, request, obj=None, **kwargs):
        form = super(PlotAdmin, self).get_form(request, obj, **kwargs)
        return form
