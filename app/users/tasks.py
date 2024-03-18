from celery import shared_task
import urllib.parse
import urllib.request
from django.conf import settings

from app.utils.constants import SMS


@shared_task
def send_sms(message, number):
    data = urllib.parse.urlencode({
        "apikey": settings.TEXT_LOCAL_API_KEY,
        "numbers": number,
        "message": message,
        "sender": "HRSOFF"  # Assume "TXTLCL" is your sender ID; adjust as necessary.
    }).encode("utf-8")
    request = urllib.request.Request(SMS.TEXTLOCAL_HOST, data)
    with urllib.request.urlopen(request) as f:
        response = f.read()
    return response

