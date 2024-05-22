from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit


class CRMLeadAdmin(admin.ModelAdmin):
    list_display = ['id', 'property', 'customer', 'assigned_so', 'current_crm_status', 'current_approval_status',
                    'is_active', 'created_at', 'updated_at']
    list_filter = ['current_crm_status', 'current_approval_status', 'created_at', 'is_active']
    search_fields = ['customer__name', 'property__name']


class StatusChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'crm_lead', 'requested_status', 'approval_status', 'date_requested', 'actioned_by', 'remarks']
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
    list_display = ('id', 'crm_lead_link', 'amount', 'payment_method_display', 'payment_status_display', 'payment_date', 'backend_reference_number')
    list_filter = ('payment_method', 'payment_status', 'payment_date')
    search_fields = ('crm_lead__id', 'reference_number', 'backend_reference_number')
    readonly_fields = ('backend_reference_number', 'created_at', 'updated_at')  # Protects auto-generated and timestamp fields
    date_hierarchy = 'payment_date'  # Easy navigation through dates
    ordering = ('-payment_date',)

    def crm_lead_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse("admin:crm_crmlead_change", args=(obj.crm_lead.pk,)), obj.crm_lead)
    crm_lead_link.short_description = "CRM Lead"

    def payment_method_display(self, obj):
        return obj.get_payment_method_display()
    payment_method_display.short_description = 'Payment Method'

    def payment_status_display(self, obj):
        return obj.get_payment_status_display()
    payment_status_display.short_description = 'Payment Status'

    fieldsets = (
        (None, {
            'fields': ('crm_lead', 'amount', 'payment_description')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'payment_status', 'payment_for', 'payment_date', 'reference_number', 'backend_reference_number')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # objects already created
            return self.readonly_fields + ('payment_method', 'payment_date')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        # Disable delete if not superuser
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        # Implement any additional logic here
        super().save_model(request, obj, form, change)


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
