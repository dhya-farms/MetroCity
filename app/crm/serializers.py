from rest_framework import serializers

from app.crm.enums import PropertyStatus, ApprovalStatus, PaymentMethod, PaymentStatus, PaymentFor
from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit
from app.properties.serializers import PlotSerializer, PropertySerializer, PhaseSerializer, PlotSerializerSimple, \
    PhaseSerializerComplex
from app.users.serializers import CustomerSerializer, UserSerializer
from app.utils.helpers import get_serialized_enum


class CRMLeadSerializer(serializers.ModelSerializer):
    property = PropertySerializer()
    phase = PhaseSerializer()
    plot = PlotSerializerSimple()
    customer = CustomerSerializer()
    assigned_so = UserSerializer()
    current_crm_status = serializers.SerializerMethodField()
    current_approval_status = serializers.SerializerMethodField()
    status_change_request = serializers.SerializerMethodField()
    is_site_visit_done = serializers.SerializerMethodField()
    is_token_advance_done = serializers.SerializerMethodField()
    is_documentation_done = serializers.SerializerMethodField()
    is_payment_done = serializers.SerializerMethodField()
    is_document_delivery_done = serializers.SerializerMethodField()

    def get_current_crm_status(self, obj: CRMLead):
        if obj.current_crm_status:
            return get_serialized_enum(PropertyStatus(obj.current_crm_status))
        return dict()

    def get_current_approval_status(self, obj: CRMLead):
        if obj.current_approval_status:
            return get_serialized_enum(ApprovalStatus(obj.current_approval_status))
        return dict()

    def get_status_change_request(self, obj: CRMLead):
        try:
            request = StatusChangeRequest.objects.get(
                crm_lead=obj,
                requested_status=obj.current_crm_status,
                approval_status=obj.current_approval_status
            )
            return StatusChangeRequestSimpleSerializer(request).data
        except StatusChangeRequest.DoesNotExist:
            return None

    def get_is_site_visit_done(self, obj: CRMLead):
        return obj.current_crm_status > PropertyStatus.SITE_VISIT or (
                obj.current_crm_status == PropertyStatus.SITE_VISIT and obj.current_approval_status == ApprovalStatus.COMPLETED)

    def get_is_token_advance_done(self, obj: CRMLead):
        return obj.current_crm_status > PropertyStatus.TOKEN_ADVANCE or (
                obj.current_crm_status == PropertyStatus.TOKEN_ADVANCE and obj.current_approval_status == ApprovalStatus.COMPLETED)

    def get_is_documentation_done(self, obj: CRMLead):
        return obj.current_crm_status > PropertyStatus.DOCUMENTATION or (
                obj.current_crm_status == PropertyStatus.DOCUMENTATION and obj.current_approval_status == ApprovalStatus.COMPLETED)

    def get_is_payment_done(self, obj: CRMLead):
        return obj.current_crm_status > PropertyStatus.PAYMENT or (
                obj.current_crm_status == PropertyStatus.PAYMENT and obj.current_approval_status == ApprovalStatus.COMPLETED)

    def get_is_document_delivery_done(self, obj: CRMLead):
        return obj.current_crm_status > PropertyStatus.DOCUMENT_DELIVERY or (
                obj.current_crm_status == PropertyStatus.DOCUMENT_DELIVERY and obj.current_approval_status == ApprovalStatus.COMPLETED)

    class Meta:
        model = CRMLead
        fields = ['id', 'property', 'phase', 'plot', 'total_amount', 'customer', 'assigned_so', 'details',
                  'current_crm_status', 'current_approval_status', 'created_at', 'updated_at',
                  'status_change_request', 'is_site_visit_done', 'is_token_advance_done',
                  'is_documentation_done', 'is_payment_done', 'is_document_delivery_done']


class StatusChangeRequestSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()
    requested_by = UserSerializer()
    actioned_by = UserSerializer()
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


class StatusChangeRequestSimpleSerializer(serializers.ModelSerializer):
    requested_by = UserSerializer()
    actioned_by = UserSerializer()
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
        fields = ["id", "crm_lead",
                  "requested_by",
                  "actioned_by",
                  "requested_status",
                  "approval_status",
                  "remarks"]


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
    payment_method = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()
    payment_for = serializers.SerializerMethodField()

    def get_payment_method(self, obj: Payment):
        if obj.payment_method:
            return get_serialized_enum(PaymentMethod(obj.payment_method))
        return dict()

    def get_payment_status(self, obj: Payment):
        if obj.payment_status:
            return get_serialized_enum(PaymentStatus(obj.payment_status))
        return dict()

    def get_payment_for(self, obj: Payment):
        if obj.payment_for:
            return get_serialized_enum(PaymentFor(obj.payment_for))
        return dict()

    class Meta:
        model = Payment
        fields = '__all__'


class SiteVisitSerializer(serializers.ModelSerializer):
    crm_lead = CRMLeadSerializer()

    class Meta:
        model = SiteVisit
        fields = '__all__'
