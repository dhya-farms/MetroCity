from django.db import models
from rest_framework import serializers

from app.properties.enums import AreaOfPurpose, PropertyType, PhaseStatus, Facing, SoilType, AreaSizeUnit, Availability
from app.properties.models import Property, Phase, Plot, PropertyImage
from app.users.serializers import UserSerializer, CustomerSerializer
from app.utils.helpers import get_serialized_enum

from rest_framework import serializers
from .models import PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'is_thumbnail', 'is_slider_image', 'slider_image_order']

    def validate(self, data):
        """
        Check that slider_image_order is provided if is_slider_image is True.
        """
        if data.get('is_slider_image') and data.get('slider_image_order') is None:
            raise serializers.ValidationError("Slider image order must be set if the image is used as a slider image.")
        return data


class PhaseSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['id', 'property', 'phase_number', 'description', 'start_date', 'estimated_completion_date', 'status']


class PhaseSerializer(serializers.ModelSerializer):
    no_of_plots = serializers.SerializerMethodField()
    area_size_from = serializers.SerializerMethodField()
    area_size_unit = serializers.SerializerMethodField()
    price_from = serializers.SerializerMethodField()

    def get_no_of_plots(self, obj):
        # Filter to count only plots that are not sold
        return obj.plots.filter(is_sold=False).count()

    def get_area_size_from(self, obj):
        # Filter to get the minimum price among unsold plots
        min_sq_ft = obj.plots.filter(is_sold=False).aggregate(models.Min('area_size'))['area_size__min']
        return min_sq_ft if min_sq_ft is not None else "No plots or no unsold plots"

    def get_area_size_unit(self, obj):
        # Filter to get the minimum price among unsold plots
        plot_first: Plot = obj.plots.first()
        if plot_first and plot_first.area_size_unit:
            return get_serialized_enum(AreaSizeUnit(plot_first.area_size_unit))
        return dict()

    def get_price_from(self, obj):
        min_price = obj.plots.filter(is_sold=False).aggregate(models.Min('price'))['price__min']

        return min_price if min_price is not None else "No Plots or No unsold plots"

    class Meta:
        model = Phase
        fields = ['id', 'property', 'phase_number', 'description', 'start_date', 'estimated_completion_date', 'status',
                  'no_of_plots', 'area_size_from', 'area_size_unit', 'price_from']


class PropertySerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    director = UserSerializer()
    current_lead = CustomerSerializer()
    property_type = serializers.SerializerMethodField()
    area_of_purpose = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)
    phases = PhaseSerializer(many=True, read_only=True)

    def get_property_type(self, obj: Property):
        if obj.property_type:
            return get_serialized_enum(PropertyType(obj.property_type))
        return dict()

    def get_area_of_purpose(self, obj: Property):
        if obj.area_of_purpose:
            return get_serialized_enum(AreaOfPurpose(obj.area_of_purpose))
        return dict()

    class Meta:
        model = Property
        fields = [
            'id',
            'property_type',
            'description',
            'area_of_purpose',
            'name',
            'details',
            'location',
            'gmap_url',
            'created_at',
            'updated_at',
            'created_by',
            'director',
            'current_lead',
            'images',
            'phases',
        ]


class PhaseSerializerComplex(serializers.ModelSerializer):
    property = PropertySerializer()
    status = serializers.SerializerMethodField()
    no_of_plots = serializers.SerializerMethodField()
    area_size_from = serializers.SerializerMethodField()
    area_size_unit = serializers.SerializerMethodField()
    price_from = serializers.SerializerMethodField()

    def get_no_of_plots(self, obj):
        # Filter to count only plots that are not sold
        return obj.plots.filter(is_sold=False).count()

    def get_area_size_from(self, obj):
        # Filter to get the minimum price among unsold plots
        min_sq_ft = obj.plots.filter(is_sold=False).aggregate(models.Min('area_size'))['area_size__min']
        return min_sq_ft if min_sq_ft is not None else "No plots or no unsold plots"

    def get_area_size_unit(self, obj):
        # Filter to get the minimum price among unsold plots
        plot_first: Plot = obj.plots.first()
        if plot_first and plot_first.area_size_unit:
            return get_serialized_enum(AreaSizeUnit(plot_first.area_size_unit))
        return dict()

    def get_status(self, obj: Phase):
        if obj.status:
            return get_serialized_enum(PhaseStatus(obj.status))
        return dict()

    def get_price_from(self, obj):

        min_price = obj.plots.filter(is_sold=False).aggregate(models.Min('price'))['price__min']

        return min_price if min_price is not None else "No Plots or No unsold plots"

    class Meta:
        model = Phase
        fields = ['id', 'property', 'phase_number', 'description', 'start_date', 'estimated_completion_date', 'status',
                  'no_of_plots', 'area_size_from', 'area_size_unit', 'price_from']


class PlotSerializer(serializers.ModelSerializer):
    phase_details = PhaseSerializerComplex(source='phase', read_only=True)
    property_details = PropertySerializer(source='phase.property', read_only=True)  # Nested property details via phase
    facing = serializers.SerializerMethodField()
    soil_type = serializers.SerializerMethodField()
    area_size_unit = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()

    def get_facing(self, obj: Plot):
        if obj.facing:
            return get_serialized_enum(Facing(obj.facing))
        return dict()

    def get_soil_type(self, obj: Plot):
        if obj.soil_type:
            return get_serialized_enum(SoilType(obj.soil_type))
        return dict()

    def get_area_size_unit(self, obj: Plot):
        if obj.area_size_unit:
            return get_serialized_enum(AreaSizeUnit(obj.area_size_unit))
        return dict()

    def get_availability(self, obj: Plot):
        if obj.availability:
            return get_serialized_enum(Availability(obj.availability))
        return dict()

    class Meta:
        model = Plot
        fields = ['id', 'plot_number', 'is_corner_site', 'dimensions', 'facing', 'soil_type', 'plantation', 'price',
                  'area_size', 'area_size_unit', 'availability', 'created_at', 'updated_at', 'is_sold', 'phase_details',
                  'property_details']


class PlotSerializerSimple(serializers.ModelSerializer):
    facing = serializers.SerializerMethodField()
    soil_type = serializers.SerializerMethodField()
    area_size_unit = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()

    def get_facing(self, obj: Plot):
        if obj.facing:
            return get_serialized_enum(Facing(obj.facing))
        return dict()

    def get_soil_type(self, obj: Plot):
        if obj.soil_type:
            return get_serialized_enum(SoilType(obj.soil_type))
        return dict()

    def get_area_size_unit(self, obj: Plot):
        if obj.area_size_unit:
            return get_serialized_enum(AreaSizeUnit(obj.area_size_unit))
        return dict()

    def get_availability(self, obj: Plot):
        if obj.availability:
            return get_serialized_enum(Availability(obj.availability))
        return dict()

    class Meta:
        model = Plot
        fields = ['id', 'phase', 'plot_number', 'is_corner_site', 'dimensions', 'facing', 'soil_type', 'plantation',
                  'price', 'area_size', 'area_size_unit', 'availability', 'created_at', 'updated_at', 'is_sold']
