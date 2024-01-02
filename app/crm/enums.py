from django.db import models


class PropertyStatus(models.IntegerChoices):
    SITE_VISIT = 1, 'Site Visit'
    TOKEN_ADVANCE = 2, 'Token Advance'
    DOCUMENTATION = 3, 'Documentation'
    PAYMENT = 4, 'Payment'
    DOCUMENT_DELIVERY = 5, 'Document Delivery'
    # Add more property statuses here if needed


class PaymentMode(models.IntegerChoices):
    GPAY = 1, 'Gpay'
    PAYTM = 2, 'PayTm'
    # Add more payment modes here if needed


class PaymentStatus(models.IntegerChoices):
    FULL = 1, 'Full'
    PARTIAL = 2, 'Partial'
    # Add more status options here if needed


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
    # Add more approval statuses here if needed

