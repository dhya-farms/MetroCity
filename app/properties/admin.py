from django.contrib import admin
from app.properties.models import Property, Phase, Plot, PropertyImage, UpdateImage, Update, Amenity, NearbyAttraction

from django.contrib import admin
from .models import PropertyImage

admin.site.register(UpdateImage)


class UpdateImageInline(admin.TabularInline):
    model = UpdateImage
    extra = 1  # Specifies the number of extra forms in the inline formset.


@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'date_posted', 'id')
    list_filter = ('date_posted', 'posted_by')
    search_fields = ('title', 'description', 'posted_by__username')
    readonly_fields = ('date_posted',)  # 'posted_by' is handled in the form

    inlines = [UpdateImageInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'posted_by')
        }),
        ('Date Information', {
            'fields': ('date_posted',),
            'classes': ('collapse',)
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        Form = super(UpdateAdmin, self).get_form(request, obj, **kwargs)
        if obj is None:
            Form.base_fields['posted_by'].queryset = Form.base_fields['posted_by'].queryset.filter(
                username=request.user.username)
            Form.base_fields['posted_by'].initial = request.user.id
        return Form

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new instance, set posted_by
            obj.posted_by = request.user
        super(UpdateAdmin, self).save_model(request, obj, form, change)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1  # Specifies the number of empty forms to display
    fields = ['image', 'is_thumbnail', 'is_slider_image', 'slider_image_order']


class PhaseInline(admin.TabularInline):
    model = Phase
    extra = 1


class PlotInline(admin.TabularInline):
    model = Plot
    extra = 1


# Inline admin for many-to-many relationships
class AmenityInline(admin.TabularInline):
    model = Property.amenities.through  # Access the automatically created through model
    extra = 1


class NearbyAttractionInline(admin.TabularInline):
    model = Property.nearby_attractions.through  # Similarly, access the through model
    extra = 1


admin.site.register(Amenity)
admin.site.register(NearbyAttraction)


# Property admin updates
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'property_type', 'location', 'rating', 'created_at', 'updated_at']
    list_filter = ['property_type', 'area_of_purpose', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'location', 'details']
    inlines = [PropertyImageInline, PhaseInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        (None, {'fields': ('name', 'description', 'details')}),
        ('Location Details', {'fields': ('location', 'gmap_url')}),
        ('Classification', {'fields': ('property_type', 'area_of_purpose')}),
        ('Administrative', {'fields': ('rating', 'created_by', 'director', 'current_lead', 'created_at', 'updated_at')}),
        ('Amenities and Attractions', {'fields': ('amenities', 'nearby_attractions')}),
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
    list_display = ['id', 'phase', 'plot_number', 'dimensions', 'is_booked', 'is_sold']
    list_filter = ['is_booked', 'is_sold', 'phase', 'availability']
    search_fields = ['plot_number']

    def get_form(self, request, obj=None, **kwargs):
        form = super(PlotAdmin, self).get_form(request, obj, **kwargs)
        return form
