from django.contrib import admin

from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit


class CRMLeadAdmin(admin.ModelAdmin):
    list_display = ['id', 'property', 'customer', 'assigned_so', 'current_status', 'created_at', 'updated_at']
    list_filter = ['current_status', 'created_at']
    search_fields = ['customer__name', 'property__name']


class StatusChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'crm_lead', 'requested_status', 'approval_status', 'date_requested', 'approved_by']
    list_filter = ['approval_status', 'date_requested']
    search_fields = ['crm_lead__customer__name']


class LeadStatusLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'crm_lead', 'previous_status', 'new_status', 'changed_by', 'change_date']
    list_filter = ['previous_status', 'new_status', 'change_date']
    search_fields = ['crm_lead__customer__name']


class SalesOfficerPerformanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'sales_officer', 'points', 'evaluation_date']
    list_filter = ['evaluation_date']
    search_fields = ['sales_officer__username']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'crm_lead', 'amount', 'payment_type', 'payment_status', 'created_at']
    list_filter = ['payment_type', 'payment_status', 'created_at']
    search_fields = ['crm_lead__customer__name', 'amount']


class SiteVisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'crm_lead', 'is_pickup', 'pickup_address', 'pickup_date', 'is_drop', 'drop_address']
    list_filter = ['is_pickup', 'is_drop', 'pickup_date']
    search_fields = ['crm_lead__customer__name', 'pickup_address']


admin.site.register(CRMLead, CRMLeadAdmin)
admin.site.register(StatusChangeRequest, StatusChangeRequestAdmin)
admin.site.register(LeadStatusLog, LeadStatusLogAdmin)
admin.site.register(SalesOfficerPerformance, SalesOfficerPerformanceAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(SiteVisit, SiteVisitAdmin)
