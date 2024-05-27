from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta
from .models import CRMLead

@shared_task
def deactivate_old_crm_leads():
    outdated_leads = CRMLead.objects.filter(
        updated_at__lt=now() - timedelta(days=90),
        is_active=True
    )
    count = outdated_leads.update(is_active=False)
    return f'Deactivated {count} leads.'
