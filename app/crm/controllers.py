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

    def create(self, **kwargs):
        try:
            instance = self.model.objects.create(**kwargs)
            instance: StatusChangeRequest = self.model.objects.select_related('crm_lead').get(id=instance.pk)
            crm_lead: CRMLead = instance.crm_lead
            crm_lead.current_crm_status = instance.requested_status
            crm_lead.current_approval_status = instance.approval_status
            crm_lead.save()
            return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)

    def edit(self, instance_id, **kwargs):
        try:
            instance: StatusChangeRequest = self.model.objects.select_related('crm_lead').get(id=instance_id)
            for attr, value in kwargs.items():
                if value:
                    setattr(instance, attr, value)
                if attr == "approval_status":
                    crm_lead: CRMLead = instance.crm_lead
                    crm_lead.current_approval_status = instance.approval_status
                    crm_lead.save()
                    if value == ApprovalStatus.APPROVED.value:
                        setattr(instance, 'date_approved', datetime.now())
                    if value == ApprovalStatus.REJECTED.value:
                        setattr(instance, 'date_rejected', datetime.now())
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
