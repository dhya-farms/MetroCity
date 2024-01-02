from enum import Enum
from django.db import models


class FileUploadStrategy(Enum):
    STANDARD = "standard"
    DIRECT = "direct"


class FileUploadStorage(Enum):
    LOCAL = "local"
    S3 = "s3"


class FileUsageType(models.IntegerChoices):
    PROPERTY_IMAGE = 1, 'Property Image'
    PROPERTY_DOCUMENT = 2, 'Property Document'
    CRM_DOCUMENT = 3, 'CRM Document'
    LAYOUT_IMAGE = 4, 'Layout Image'
    # Other file types...


class CRMDocumentType(models.IntegerChoices):
    PAN = 1, 'PAN Card'
    AADHAR = 2, 'Aadhar Card'
    OTHER = 3, 'Other'
    # Other CRM document types...

