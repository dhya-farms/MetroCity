from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.crm.enums import PropertyStatus, ApprovalStatus, PaymentMethod
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal
from app.crm.enums import PaymentMode, PaymentStatus, PaymentFor


def parse_datetime(v):
    if v:
        try:
            return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as e:
            raise ValueError(f"time format is incorrect: {e}")
    return v


# CRMLead Creation Schema
class CRMLeadCreateSchema(BaseModel):
    property_id: int
    phase_id: int
    plot_id: Optional[int]
    customer_id: int
    assigned_so_id: int
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)
    current_crm_status: Optional[PropertyStatus]
    current_approval_status: Optional[ApprovalStatus]

    # Validator to allow string version of enum value too
    _validate_current_crm_status = validator('current_crm_status',
                                             allow_reuse=True,
                                             pre=True)(allow_string_rep_of_enum)

    _validate_current_approval_status = validator('current_approval_status',
                                                  allow_reuse=True,
                                                  pre=True)(allow_string_rep_of_enum)


# CRMLead Update Schema
class CRMLeadUpdateSchema(BaseModel):
    phase_id: Optional[int]
    plot_id: Optional[int]
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)
    current_crm_status: Optional[PropertyStatus]
    current_approval_status: Optional[ApprovalStatus]

    # Validator to allow string version of enum value too
    _validate_current_crm_status = validator('current_crm_status',
                                             allow_reuse=True,
                                             pre=True)(allow_string_rep_of_enum)

    _validate_current_approval_status = validator('current_approval_status',
                                                  allow_reuse=True,
                                                  pre=True)(allow_string_rep_of_enum)


# CRMLead Listing Schema
class CRMLeadListSchema(BaseModel):
    property_id: Optional[int]
    phase_id: Optional[int]
    plot_id: Optional[int]
    customer_id: Optional[int]
    assigned_so_id: Optional[int]
    current_crm_status: Optional[PropertyStatus]
    current_approval_status: Optional[ApprovalStatus]

    # Validator to allow string version of enum value too
    _validate_current_crm_status = validator('current_crm_status',
                                             allow_reuse=True,
                                             pre=True)(allow_string_rep_of_enum)

    _validate_current_approval_status = validator('current_approval_status',
                                                  allow_reuse=True,
                                                  pre=True)(allow_string_rep_of_enum)


# StatusChangeRequest Creation Schema
class StatusChangeRequestCreateSchema(BaseModel):
    crm_lead_id: int
    requested_by_id: int
    actioned_by_id: Optional[int]
    requested_status: PropertyStatus
    approval_status: Optional[ApprovalStatus]
    remarks: Optional[str]
    date_approved: Optional[datetime]
    date_rejected: Optional[datetime]

    @validator('date_approved', 'date_rejected', pre=True, allow_reuse=True)
    def validate_date_approved_rejected(cls, v):
        return parse_datetime(v)

    # Validator to allow string version of enum value too
    _validate_enums = validator('approval_status', 'requested_status',
                                allow_reuse=True,
                                pre=True)(allow_string_rep_of_enum)


# StatusChangeRequest Update Schema
class StatusChangeRequestUpdateSchema(BaseModel):
    actioned_by_id: Optional[int]
    approval_status: Optional[ApprovalStatus]
    remarks: Optional[str]

    # Validator to allow string version of enum value too
    _validate_enums = validator('approval_status',
                                allow_reuse=True,
                                pre=True)(allow_string_rep_of_enum)


# StatusChangeRequest Listing Schema
class StatusChangeRequestListSchema(BaseModel):
    crm_lead_id: Optional[int]
    requested_by_id: Optional[int]
    actioned_by_id: Optional[int]
    requested_status: Optional[PropertyStatus]
    approval_status: Optional[ApprovalStatus]

    # Validator to allow string version of enum value too
    _validate_enums = validator('approval_status', 'requested_status',
                                allow_reuse=True,
                                pre=True)(allow_string_rep_of_enum)


# Payment Creation Schema
class PaymentCreateSchema(BaseModel):
    crm_lead_id: int
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    payment_method: PaymentMethod
    payment_status: Optional[PaymentStatus] = PaymentStatus.COMPLETED
    payment_for: PaymentFor
    payment_description: Optional[str]
    reference_number: Optional[str]

    # Validator to allow string version of enum value too
    _validate_enums = validator('payment_method', 'payment_status', 'payment_for',
                                allow_reuse=True,
                                pre=True)(allow_string_rep_of_enum)


class PaymentUpdateSchema(PaymentCreateSchema):
    pass


class PaymentListSchema(BaseModel):
    crm_lead_id: Optional[int]
    payment_method: Optional[PaymentMethod]
    payment_status: Optional[PaymentStatus]
    payment_for: Optional[PaymentFor]
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    @validator('start_time', 'end_time', pre=True, allow_reuse=True)
    def validate_time(cls, v):
        return parse_datetime(v)

    _validate_enums = validator('payment_method', 'payment_status', 'payment_for',
                                allow_reuse=True, pre=True)(allow_string_rep_of_enum)


# SiteVisit Creation Schema
class SiteVisitCreateSchema(BaseModel):
    crm_lead_id: int
    is_pickup: bool
    pickup_address: Optional[str]
    pickup_date: Optional[datetime]
    is_drop: bool
    drop_address: Optional[str]

    @validator('pickup_date', pre=True, allow_reuse=True)
    def validate_pickup_date(cls, v):
        return parse_datetime(v)


# SiteVisit Update Schema
class SiteVisitUpdateSchema(BaseModel):
    crm_lead_id: int
    is_pickup: bool
    pickup_address: Optional[str]
    pickup_date: Optional[datetime]
    is_drop: bool
    drop_address: Optional[str]

    @validator('pickup_date', pre=True, allow_reuse=True)
    def validate_pickup_date(cls, v):
        return parse_datetime(v)


# SiteVisit List Schema
class SiteVisitListSchema(BaseModel):
    crm_lead_id: Optional[int]
    is_pickup: Optional[bool]
    pickup_date: Optional[datetime]
    is_drop: Optional[bool]

    @validator('pickup_date', pre=True, allow_reuse=True)
    def validate_pickup_date(cls, v):
        return parse_datetime(v)
