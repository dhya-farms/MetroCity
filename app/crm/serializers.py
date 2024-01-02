from rest_framework import serializers
from .models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit
from ..properties.serializers import PlotSerializer
from ..users.serializers import CustomerSerializer, UserSerializer


class CRMLeadSerializer(serializers.ModelSerializer):
    plot = PlotSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = CRMLead
        fields = '__all__'


class StatusChangeRequestSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()
    requested_by = UserSerializer()
    approved_by = UserSerializer()

    class Meta:
        model = StatusChangeRequest
        fields = '__all__'


class LeadStatusLogSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer()
    crm_lead = CRMLeadSerializer()

    class Meta:
        model = LeadStatusLog
        fields = '__all__'


class SalesOfficerPerformanceSerializer(serializers.ModelSerializer):
    sales_officer = UserSerializer()

    class Meta:
        model = SalesOfficerPerformance
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class SiteVisitSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()

    class Meta:
        model = SiteVisit
        fields = '__all__'
