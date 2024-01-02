from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from app.crm.enums import PropertyStatus, PaymentMode, PaymentStatus, PaymentFor, DocumentStatus, ApprovalStatus

User = get_user_model()


class CRMLead(models.Model):
    plot = models.ForeignKey("properties.Plot", on_delete=models.CASCADE)
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    assigned_so = models.ForeignKey(User, related_name='assigned_crm_leads', on_delete=models.CASCADE, blank=True, null=True)
    initial_contact_date = models.DateTimeField(blank=True, null=True)
    current_status = models.IntegerField(choices=PropertyStatus.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StatusChangeRequest(models.Model):
    crm_lead = models.ForeignKey(CRMLead, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, related_name='requested_changes', on_delete=models.CASCADE, blank=True, null=True)
    approved_by = models.ForeignKey(User, related_name='approved_changes', on_delete=models.CASCADE, blank=True, null=True)
    requested_status = models.IntegerField(choices=PropertyStatus.choices, blank=True, null=True)
    approval_status = models.IntegerField(choices=ApprovalStatus.choices, blank=True, null=True)
    date_requested = models.DateTimeField(blank=True, null=True)
    date_approved_rejected = models.DateTimeField(blank=True, null=True)


class LeadStatusLog(models.Model):
    previous_status = models.IntegerField( choices=PropertyStatus.choices, blank=True, null=True)
    new_status = models.IntegerField(choices=PropertyStatus.choices, blank=True, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    crm_lead = models.ForeignKey(CRMLead, on_delete=models.CASCADE)


class SalesOfficerPerformance(models.Model):
    sales_officer = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(blank=True, null=True)
    performance_metrics = JSONField(blank=True, null=True)
    evaluation_date = models.DateTimeField(blank=True, null=True)


class Payment(models.Model):
    crm_lead = models.ForeignKey(CRMLead, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_mode = models.IntegerField( choices=PaymentMode.choices, blank=True, null=True)
    payment_count = models.IntegerField(default=1)
    payment_status = models.IntegerField( choices=PaymentStatus.choices, blank=True, null=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_for = models.IntegerField( choices=PaymentFor.choices, blank=True, null=True)
    payment_detail = models.CharField(max_length=45, blank=True, null=True)
    reference_number = models.CharField(max_length=45, blank=True, null=True)


class SiteVisit(models.Model):
    crm_lead = models.ForeignKey(CRMLead, on_delete=models.CASCADE)
    is_pickup = models.BooleanField(default=False)
    pickup_address = models.TextField(blank=True, null=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    is_drop = models.BooleanField(default=False)
    drop_address = models.CharField(max_length=45, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
