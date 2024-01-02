from django.db import models
from enum import unique


@unique
class Role(models.IntegerChoices):
    ORGANIZATION_ADMIN = 1, 'Organization Admin'
    DIRECTOR = 2, 'Director'
    SALES_OFFICER = 3, 'Sales Officer'
    CUSTOMER = 4, 'Customer'
