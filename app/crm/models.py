from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from app.crm.enums import PropertyStatus, PaymentMode, PaymentStatus, PaymentFor, DocumentStatus, ApprovalStatus, \
    PaymentMethod

User = get_user_model()


class CRMLead(models.Model):
    property = models.ForeignKey("properties.Property", on_delete=models.CASCADE)
    customer = models.ForeignKey("users.Customer", on_delete=models.CASCADE)
    assigned_so = models.ForeignKey(User, related_name='assigned_crm_leads', on_delete=models.CASCADE, blank=True, null=True)
    details = JSONField(blank=True, null=True)  # Store type-specific details
    current_status = models.IntegerField(choices=PropertyStatus.choices, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CRM Lead {self.id} Property-{self.property.name} Customer-{self.customer.name} SO-{self.assigned_so.name}"


class StatusChangeRequest(models.Model):
    crm_lead = models.ForeignKey(CRMLead, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, related_name='requested_changes', on_delete=models.CASCADE, blank=True, null=True)
    approved_by = models.ForeignKey(User, related_name='approved_changes', on_delete=models.CASCADE, blank=True, null=True)
    requested_status = models.IntegerField(choices=PropertyStatus.choices, blank=True, null=True)
    approval_status = models.IntegerField(choices=ApprovalStatus.choices, blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_rejected = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"StatusChangeRequest {self.id} requested_by-{self.requested_by.name} requested_status-{self.requested_status}"


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
    payment_type = models.IntegerField(choices=PaymentMode.choices)
    # offline payment fields
    payment_status = models.IntegerField(choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_date = models.DateTimeField(blank=True, null=True)
    payment_for = models.IntegerField(choices=PaymentFor.choices)
    payment_description = models.CharField(max_length=45, blank=True, null=True)
    reference_number = models.CharField(max_length=45, blank=True, null=True)
    # online payment fields
    online_payment_method = models.PositiveSmallIntegerField(choices=PaymentMethod.choices, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature_id = models.CharField(max_length=128, null=True, blank=True)
    razorpay_invoice_id = models.CharField(max_length=100, null=True, blank=True)
    invoice_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    online_payment_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} ({self.amount} {self.payment_type})"


class SiteVisit(models.Model):
    crm_lead = models.ForeignKey(CRMLead, on_delete=models.CASCADE)
    is_pickup = models.BooleanField(default=False)
    pickup_address = models.TextField(blank=True, null=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    is_drop = models.BooleanField(default=False)
    drop_address = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
