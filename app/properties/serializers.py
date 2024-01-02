from rest_framework import serializers
from .models import Property, Phase, Plot
from ..users.serializers import UserSerializer, CustomerSerializer


class PropertySerializer(serializers.ModelSerializer):
    created_by = UserSerializer()
    director = UserSerializer()
    current_lead = CustomerSerializer()

    class Meta:
        model = Property
        fields = '__all__'  # List all fields or specify fields


class PhaseSerializer(serializers.ModelSerializer):
    property = PropertySerializer()

    class Meta:
        model = Phase
        fields = '__all__'  # List all fields or specify fields


class PlotSerializer(serializers.ModelSerializer):
    phase = PhaseSerializer()

    class Meta:
        model = Plot
        fields = '__all__'  # List all fields or specify fields
