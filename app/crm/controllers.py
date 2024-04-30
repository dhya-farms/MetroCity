from datetime import datetime

from app.crm.enums import PropertyStatus, ApprovalStatus
from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit
from django.db import IntegrityError

from app.utils.controllers import Controller
from app.utils.helpers import get_serialized_exception


class CRMLeadController(Controller):
    def __init__(self):
        self.model = CRMLead


class StatusChangeRequestController(Controller):
    def __init__(self):
        self.model = StatusChangeRequest

    def edit(self, instance_id, **kwargs):
        try:
            instance = self.model.objects.get(id=instance_id)
            for attr, value in kwargs.items():
                if attr == "approval_status" and value == ApprovalStatus.APPROVED.value:
                    setattr(instance, 'date_approved', datetime.now())
                if attr == "approval_status" and value == ApprovalStatus.REJECTED.value:
                    setattr(instance, 'date_rejected', datetime.now())
                if value:
                    setattr(instance, attr, value)
            instance.save()
            return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)


class LeadStatusLogController(Controller):
    def __init__(self):
        self.model = LeadStatusLog


class SalesOfficerPerformanceController(Controller):
    def __init__(self):
        self.model = SalesOfficerPerformance


class PaymentController(Controller):
    def __init__(self):
        self.model = Payment


class SiteVisitController(Controller):
    def __init__(self):
        self.model = SiteVisit

    def create(self, **kwargs):
        try:
            instance: SiteVisit = self.model.objects.create(**kwargs)
            StatusChangeRequestController().create(
                crm_lead=instance.crm_lead,
                requested_by=instance.crm_lead.assigned_so,
                requested_status=PropertyStatus.SITE_VISIT,
                approval_status=ApprovalStatus.PENDING
            )
            return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)


