from rest_framework import serializers

from app.crm.enums import PropertyStatus, ApprovalStatus
from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit
from app.properties.serializers import PlotSerializer, PropertySerializer
from app.users.serializers import CustomerSerializer, UserSerializer
from app.utils.helpers import get_serialized_enum


class CRMLeadSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    customer = CustomerSerializer()
    assigned_so = UserSerializer()
    current_status = serializers.SerializerMethodField()

    def get_current_status(self, obj: CRMLead):
        if obj.current_status:
            return get_serialized_enum(PropertyStatus(obj.current_status))
        return dict()

    class Meta:
        model = CRMLead
        fields = '__all__'


class StatusChangeRequestSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()
    requested_by = UserSerializer()
    approved_by = UserSerializer()
    requested_status = serializers.SerializerMethodField()
    approval_status = serializers.SerializerMethodField()

    def get_requested_status(self, obj: StatusChangeRequest):
        if obj.requested_status:
            return get_serialized_enum(PropertyStatus(obj.requested_status))
        return dict()

    def get_approval_status(self, obj: StatusChangeRequest):
        if obj.approval_status:
            return get_serialized_enum(ApprovalStatus(obj.approval_status))
        return dict()

    class Meta:
        model = StatusChangeRequest
        fields = '__all__'


class LeadStatusLogSerializer(serializers.ModelSerializer):
    changed_by = UserSerializer()
    crm_lead = CRMLeadSerializer()
    previous_status = serializers.SerializerMethodField()
    new_status = serializers.SerializerMethodField()

    def get_previous_status(self, obj: LeadStatusLog):
        if obj.previous_status:
            return get_serialized_enum(PropertyStatus(obj.previous_status))
        return dict()

    def get_new_status(self, obj: LeadStatusLog):
        if obj.new_status:
            return get_serialized_enum(PropertyStatus(obj.new_status))
        return dict()

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
    payment_type = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    payment_for = serializers.SerializerMethodField()
    online_payment_method = serializers.SerializerMethodField()

    def get_payment_type(self, obj: Payment):
        if obj.payment_type:
            return get_serialized_enum(PropertyStatus(obj.payment_type))
        return dict()

    def get_payment_status(self, obj: Payment):
        if obj.payment_status:
            return get_serialized_enum(PropertyStatus(obj.payment_status))
        return dict()

    def get_payment_for(self, obj: Payment):
        if obj.payment_for:
            return get_serialized_enum(PropertyStatus(obj.payment_for))
        return dict()

    def get_online_payment_method(self, obj: Payment):
        if obj.online_payment_method:
            return get_serialized_enum(PropertyStatus(obj.online_payment_method))
        return dict()

    class Meta:
        model = Payment
        fields = '__all__'


class SiteVisitSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()

    class Meta:
        model = SiteVisit
        fields = '__all__'
