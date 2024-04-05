from django.contrib.auth import get_user_model
from django.db import models

from app.properties.enums import Facing, SoilType
from app.properties.enums import Availability, PropertyType, AreaSizeUnit, AreaOfPurpose, PhaseStatus

User = get_user_model()


class Property(models.Model):
    property_type = models.IntegerField(choices=PropertyType.choices)
    plots_available = models.IntegerField(blank=True, null=True)
    sq_ft_from = models.CharField(blank=True, null=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    area_of_purpose = models.IntegerField(choices=AreaOfPurpose.choices, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    dtcp_details = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    amenities = models.JSONField(blank=True, null=True)
    nearby_attractions = models.JSONField(blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    phase_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_properties', blank=True, null=True,
                                   on_delete=models.CASCADE)
    director = models.ForeignKey(User, related_name='directed_properties', on_delete=models.CASCADE,
                                 blank=True, null=True)
    current_lead = models.ForeignKey("users.Customer", on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="property")


class Phase(models.Model):
    property = models.ForeignKey("properties.Property", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="phases")
    phase_number = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    estimated_completion_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=PhaseStatus.choices, blank=True,
                                 null=True)


class Plot(models.Model):
    phase = models.ForeignKey("properties.Phase", on_delete=models.CASCADE, blank=True, null=True, related_name="plots")
    plot_number = models.IntegerField(blank=True, null=True)
    is_corner_site = models.BooleanField(blank=True, null=True)
    dimensions = models.CharField(max_length=45, blank=True, null=True)
    facing = models.IntegerField(choices=Facing.choices, blank=True, null=True)
    soil_type = models.IntegerField(choices=SoilType.choices, blank=True, null=True)
    plantation = models.CharField(max_length=45, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_size = models.PositiveBigIntegerField(default=0)
    area_size_unit = models.IntegerField(choices=AreaSizeUnit.choices, null=True, blank=True)
    availability = models.IntegerField(choices=Availability.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
