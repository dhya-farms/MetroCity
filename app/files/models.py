from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

from app.common.models import BaseModel
from app.files.enums import FileUploadStorage, FileUsageType, CRMDocumentType
from app.files.utils import file_generate_upload_path

User = get_user_model()


class File(BaseModel):
    file = models.FileField(
        upload_to=file_generate_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'pdf', 'doc', 'docx'])]
    )

    original_file_name = models.TextField()

    file_name = models.CharField(max_length=255, unique=True)
    file_type = models.CharField(max_length=255)
    file_usage_type = models.IntegerField(choices=FileUsageType.choices, blank=True, null=True)

    # CRM Document Type - only applicable if file_type is CRM_DOCUMENT
    crm_document_type = models.IntegerField(
        choices=CRMDocumentType.choices,
        blank=True,
        null=True
    )

    crm_lead = models.ForeignKey(
        "crm.CRMLead",
        related_name='files',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # As a specific behavior,
    # We might want to preserve files after the uploader has been deleted.
    # In case you want to delete the files too, use models.CASCADE & drop the null=True
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_files'
    )

    upload_finished_at = models.DateTimeField(blank=True, null=True)

    @property
    def is_valid(self):
        """
        We consider a file "valid" if the the datetime flag has value.
        """
        return bool(self.upload_finished_at)

    @property
    def url(self):
        if settings.FILE_UPLOAD_STORAGE == FileUploadStorage.S3:
            return self.file.url

        return f"{settings.APP_DOMAIN}{self.file.url}"
