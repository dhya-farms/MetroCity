from rest_framework import serializers

from app.properties.enums import AreaOfPurpose, PropertyType
from app.properties.models import Property, Phase, Plot, PropertyImage
from app.users.serializers import UserSerializer, CustomerSerializer
from app.utils.helpers import get_serialized_enum


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']


class PropertySerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    director = UserSerializer()
    current_lead = CustomerSerializer()
    property_type = serializers.SerializerMethodField()
    area_of_purpose = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)

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
            'price',
            'details',
            'location',
            'gmap_url',
            'created_at',
            'updated_at',
            'created_by',
            'director',
            'current_lead',
            'images'
        ]


class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['id', 'property', 'phase_number', 'description', 'start_date', 'estimated_completion_date', 'status']


class PlotSerializer(serializers.ModelSerializer):
    phase_details = PhaseSerializer(source='phase', read_only=True)
    property_details = PropertySerializer(source='phase.property', read_only=True)  # Nested property details via phase

    class Meta:
        model = Plot
        fields = ['id', 'plot_number', 'is_corner_site', 'dimensions', 'facing', 'soil_type', 'plantation', 'price', 'area_size', 'area_size_unit', 'availability', 'created_at', 'updated_at', 'is_sold', 'phase_details', 'property_details']
