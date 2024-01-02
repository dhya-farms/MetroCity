from django.contrib import admin
from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit


@admin.register(CRMLead)
class CRMLeadAdmin(admin.ModelAdmin):
    list_display = ('plot', 'customer', 'initial_contact_date', 'current_status', 'created_at', 'updated_at')
    search_fields = ('customer__name', 'plot__name')
    list_filter = ('current_status', 'created_at')


@admin.register(StatusChangeRequest)
class StatusChangeRequestAdmin(admin.ModelAdmin):
    list_display = ('crm_lead', 'requested_by', 'approved_by', 'requested_status', 'approval_status', 'date_requested',
                    'date_approved_rejected')
    list_filter = ('requested_status', 'approval_status', 'date_requested')


@admin.register(LeadStatusLog)
class LeadStatusLogAdmin(admin.ModelAdmin):
    list_display = ('crm_lead', 'previous_status', 'new_status', 'changed_by', 'change_date', 'remarks')
    list_filter = ('previous_status', 'new_status', 'change_date')


@admin.register(SalesOfficerPerformance)
class SalesOfficerPerformanceAdmin(admin.ModelAdmin):
    list_display = ('sales_officer', 'points', 'performance_metrics', 'evaluation_date')
    search_fields = ('sales_officer__username',)
    list_filter = ('evaluation_date',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
    'crm_lead', 'amount', 'payment_mode', 'payment_status', 'payment_date', 'payment_for', 'payment_detail',
    'reference_number')
    search_fields = ('crm_lead__id',)
    list_filter = ('payment_mode', 'payment_status', 'payment_date')


@admin.register(SiteVisit)
class SiteVisitAdmin(admin.ModelAdmin):
    list_display = (
    'crm_lead', 'is_pickup', 'pickup_address', 'pickup_date', 'is_drop', 'drop_address', 'feedback', 'created_at',
    'updated_at')
    list_filter = ('is_pickup', 'is_drop', 'pickup_date')
