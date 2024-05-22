from datetime import datetime

from app.crm.enums import PropertyStatus, ApprovalStatus, PaymentFor, PaymentStatus
from app.crm.models import CRMLead, StatusChangeRequest, LeadStatusLog, SalesOfficerPerformance, Payment, SiteVisit
from django.db import IntegrityError, transaction

from app.crm.schemas import PaymentCreateSchema
from app.properties.controllers import PlotController
from app.properties.models import Plot
from app.utils.controllers import Controller
from app.utils.helpers import get_serialized_exception


class CRMLeadController(Controller):
    def __init__(self):
        self.model = CRMLead

    def edit(self, instance_id, **kwargs):
        try:
            with transaction.atomic():
                instance: CRMLead = self.model.objects.get(id=instance_id)

                # Update plot if plot_id is provided
                plot_id = kwargs.get('plot_id')
                if plot_id:
                    selected_plot: Plot = PlotController().get_instance_by_pk(plot_id)
                    if selected_plot:
                        selected_plot.is_sold = True
                        selected_plot.save()

                # Update instance attributes
                for attr, value in kwargs.items():
                    if attr != 'plot_id' and value:
                        setattr(instance, attr, value)

                # Handle status change request
                if (kwargs.get('current_crm_status') == PropertyStatus.DOCUMENTATION.value and
                    kwargs.get('current_approval_status') == ApprovalStatus.PENDING.value):
                    StatusChangeRequestController().create(
                        crm_lead=instance,
                        requested_by=instance.assigned_so,
                        requested_status=instance.current_crm_status,
                        approval_status=instance.current_approval_status
                    )

                instance.save()
                return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)


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
            with transaction.atomic():
                instance: StatusChangeRequest = self.model.objects.select_related('crm_lead').get(id=instance_id)
                crm_lead: CRMLead = instance.crm_lead

                # Update instance attributes
                for attr, value in kwargs.items():
                    if value:
                        setattr(instance, attr, value)

                if 'approval_status' in kwargs:
                    approval_status = kwargs['approval_status']
                    crm_lead.current_approval_status = approval_status
                    crm_lead.save()

                    payment_updates = []

                    if approval_status == ApprovalStatus.APPROVED.value:
                        if instance.requested_status == PropertyStatus.TOKEN_ADVANCE:
                            token_payment = Payment.objects.filter(
                                crm_lead=crm_lead, payment_for=PaymentFor.TOKEN.value
                            ).first()
                            if token_payment:
                                token_payment.payment_status = PaymentStatus.COMPLETED
                                payment_updates.append(token_payment)
                        if instance.requested_status == PropertyStatus.PAYMENT:
                            balance_payments = Payment.objects.filter(
                                crm_lead=crm_lead, payment_for=PaymentFor.BALANCE.value
                            )
                            for payment in balance_payments:
                                payment.payment_status = PaymentStatus.COMPLETED
                                payment_updates.append(payment)
                        instance.date_approved = datetime.now()

                    elif approval_status == ApprovalStatus.REJECTED.value:
                        if instance.requested_status == PropertyStatus.TOKEN_ADVANCE:
                            token_payment = Payment.objects.filter(
                                crm_lead=crm_lead, payment_for=PaymentFor.TOKEN.value
                            ).first()
                            if token_payment:
                                token_payment.payment_status = PaymentStatus.FAILED
                                payment_updates.append(token_payment)
                        if instance.requested_status == PropertyStatus.PAYMENT:
                            balance_payments = Payment.objects.filter(
                                crm_lead=crm_lead, payment_for=PaymentFor.BALANCE.value
                            )
                            for payment in balance_payments:
                                payment.payment_status = PaymentStatus.FAILED
                                payment_updates.append(payment)
                        instance.date_rejected = datetime.now()

                    # Bulk update payments
                    if payment_updates:
                        Payment.objects.bulk_update(payment_updates, ['payment_status'])

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

    def create(self, **kwargs):
        try:
            with transaction.atomic():
                instance: Payment = self.model.objects.create(**kwargs)

                crm_lead: CRMLead = instance.crm_lead
                payment_for = kwargs.get('payment_for')

                if payment_for == PaymentFor.TOKEN.value:
                    StatusChangeRequestController().create(
                        crm_lead=crm_lead,
                        requested_by=crm_lead.assigned_so,
                        requested_status=PropertyStatus.TOKEN_ADVANCE,
                        approval_status=ApprovalStatus.PENDING
                    )
                    crm_lead.current_crm_status = PropertyStatus.TOKEN_ADVANCE
                    crm_lead.current_approval_status = ApprovalStatus.PENDING
                    crm_lead.save()

                elif payment_for == PaymentFor.BALANCE.value:
                    balance_payments_count = Payment.objects.filter(
                        crm_lead=crm_lead, payment_for=PaymentFor.BALANCE.value
                    ).count()

                    if balance_payments_count == 1:
                        crm_lead.current_crm_status = PropertyStatus.PAYMENT
                        crm_lead.current_approval_status = ApprovalStatus.PENDING
                        crm_lead.save()

                return None, instance

        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)


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
            crm_lead: CRMLead = instance.crm_lead
            crm_lead.current_crm_status = PropertyStatus.SITE_VISIT
            crm_lead.current_approval_status = ApprovalStatus.PENDING
            crm_lead.save()
            return None, instance
        except (IntegrityError, ValueError) as e:
            return get_serialized_exception(e)
