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
