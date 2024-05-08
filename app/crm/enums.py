from django.db import models


class PropertyStatus(models.IntegerChoices):
    SITE_VISIT = 1, 'Site Visit'
    TOKEN_ADVANCE = 2, 'Token Advance'
    DOCUMENTATION = 3, 'Documentation'
    PAYMENT = 4, 'Payment'
    DOCUMENT_DELIVERY = 5, 'Document Delivery'
    # Add more property statuses here if needed


class PaymentMode(models.IntegerChoices):
    ONLINE = 1, 'Online'
    CASH = 2, 'Cash'


class PaymentMethod(models.IntegerChoices):
    CREDIT_CARD = 1, 'Credit Card'
    DEBIT_CARD = 2, 'Debit Card'
    NET_BANKING = 3, 'Net Banking'
    UPI = 4, 'UPI'
    RAZORPAY = 5, 'Razorpay'


class PaymentStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    COMPLETED = 2, 'Completed'
    FAILED = 3, 'Failed'


class RazorpayWebhookEventType(models.IntegerChoices):
    PAYMENT_CAPTURED = 1, 'Payment Captured'
    PAYMENT_FAILED = 2, 'Payment Failed'
    REFUND_INITIATED = 3, 'Refund Initiated'
    REFUND_FAILED = 4, 'Refund Failed'


class PaymentFor(models.IntegerChoices):
    TOKEN = 1, 'Token'
    VISIT = 2, 'Visit'
    ADVANCE = 3, 'Advance'
    FULL_PAY = 4, 'Full Pay'
    # Add more categories here if needed


class DocumentStatus(models.IntegerChoices):
    UPLOADED = 1, 'Uploaded'
    VERIFIED = 2, 'Verified'
    DELIVERED = 3, 'Delivered'
    # Add more statuses here if needed


class ApprovalStatus(models.IntegerChoices):
    PENDING = 1, 'Pending'
    APPROVED = 2, 'Approved'
    REJECTED = 3, 'Rejected'
    UNDER_REVIEW = 4, 'Under Review'
    COMPLETED = 5, 'Completed'
    # Add more approval statuses here if needed

