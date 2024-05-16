import os
import pathlib
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.urls import reverse


def file_generate_name(original_file_name):
    extension = pathlib.Path(original_file_name).suffix

    return f"{uuid4().hex}{extension}"


def file_generate_upload_path(instance, filename):
    # Ensure that instance.file_name is correctly set
    if not instance.file_name:
        raise SuspiciousFileOperation("File name not set in instance.")

    # Generate the upload path
    return os.path.join("files", instance.file_name)


def file_generate_local_upload_url(*, file_id: str):
    url = reverse("api:files:upload:direct:local", kwargs={"file_id": file_id})

    app_domain: str = settings.APP_DOMAIN  # type: ignore

    return f"{app_domain}{url}"


def bytes_to_mib(value: int) -> float:
    # 1 bytes = 9.5367431640625E-7 mebibytes
    return value * 9.5367431640625e-7
