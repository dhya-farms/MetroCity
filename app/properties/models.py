from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import JSONField, Case, When, Value

from app.properties.enums import Facing, SoilType
from app.properties.enums import Availability, PropertyType, AreaSizeUnit, AreaOfPurpose, PhaseStatus

User = get_user_model()


class Update(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(User, related_name='updates', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.posted_by}"


class UpdateImage(models.Model):
    update = models.ForeignKey(Update, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='update_images/')

    def __str__(self):
        return f"Image for {self.update.title}"


class Property(models.Model):
    property_type = models.IntegerField(choices=PropertyType.choices)
    description = models.TextField(blank=True, null=True)
    area_of_purpose = models.IntegerField(choices=AreaOfPurpose.choices, null=True, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    details = JSONField(blank=True, null=True)  # Store type-specific details
    location = models.TextField(blank=True, null=True)
    gmap_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_properties', blank=True, null=True,
                                   on_delete=models.CASCADE)
    director = models.ForeignKey(User, related_name='directed_properties', on_delete=models.CASCADE,
                                 blank=True, null=True)
    current_lead = models.ForeignKey("users.Customer", on_delete=models.CASCADE, blank=True, null=True,
                                     related_name="properties")

    def __str__(self):
        return f"{self.id} ({self.name})"


class PropertyImage(models.Model):
    property = models.ForeignKey('Property', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_images/')
    is_slider_image = models.BooleanField(default=False, blank=True, null=True, verbose_name='Use as slider image')
    is_thumbnail = models.BooleanField(default=False, blank=True, null=True, verbose_name='Use as Home screen image')
    slider_image_order = models.IntegerField(blank=True, null=True, verbose_name='Slider Image Order')

    class Meta:
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'
        ordering = [
            Case(
                When(is_slider_image=True, then=Value(0)),
                default=Value(1),
                output_field=models.IntegerField(),
            ),
            'slider_image_order',  # This sorts slider images by their order
        ]

    def __str__(self):
        return f"{self.property.name} Image"

    def clean(self):
        """
        Ensure that if is_slider_image is True, then slider_image_order is not None.
        """
        if self.is_slider_image and self.slider_image_order is None:
            raise ValidationError("Slider image order must be provided if the image is used as a slider image.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        """
        Ensure that if is_slider_image is True, then slider_image_order is not None.
        """
        if self.is_slider_image and self.slider_image_order is None:
            raise ValidationError("Slider image order must be provided if the image is used as a slider image.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# Example data for a DTCP PLOTS property
# property_data = {
#     "property_type": PropertyType.DTCP_PLOTS,
#     "name": "Sunshine Plots",
#     "price": 500000.00,
#     "location": "Near Lakeview",
#     "details": json.dumps({
#         "plots_available": 15,
#         "sq_ft_from": "1200",
#         "dtcp_details": "Approved for residential development",
#         "amenities": ["Electricity", "Water supply"],
#         "nearby_attractions": ["Lake", "Community Park"]
#     })
# }


class Phase(models.Model):
    property = models.ForeignKey("properties.Property", on_delete=models.CASCADE, blank=True, null=True,
                                 related_name="phases")
    phase_number = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    estimated_completion_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=PhaseStatus.choices, default=PhaseStatus.NOT_COMPLETED, blank=True,
                                 null=True)

    def __str__(self):
        return f"Phase - {self.phase_number} -- {self.property.name} Image"


class Plot(models.Model):
    phase = models.ForeignKey("properties.Phase", on_delete=models.CASCADE, blank=True, null=True, related_name="plots")
    plot_number = models.IntegerField(blank=True, null=True)
    is_corner_site = models.BooleanField(default=False, blank=True, null=True)
    dimensions = models.CharField(max_length=45, blank=True, null=True)
    facing = models.IntegerField(choices=Facing.choices, blank=True, null=True)
    soil_type = models.IntegerField(choices=SoilType.choices, blank=True, null=True)
    plantation = models.CharField(max_length=45, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_size = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    area_size_unit = models.IntegerField(choices=AreaSizeUnit.choices, null=True, blank=True)
    availability = models.IntegerField(choices=Availability.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.phase.property.name} Phase - {self.phase.phase_number} Plot - {self.plot_number}"
