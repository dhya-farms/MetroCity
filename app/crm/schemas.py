from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal
from typing import Optional
from datetime import datetime
from app.crm.enums import PropertyStatus, ApprovalStatus
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal
from app.crm.enums import PaymentMode, PaymentStatus, PaymentFor


# CRMLead Creation Schema
class CRMLeadCreateSchema(BaseModel):
    plot_id: int
    customer_id: int
    assigned_so_id: int
    initial_contact_date: Optional[str]
    current_status: Optional[PropertyStatus]

    def get_initial_contact_date(self):
        if self.initial_contact_date:
            try:
                time_obj = datetime.strptime(self.initial_contact_date, '%Y-%m-%dT%H:%M:%SZ')
                return time_obj
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return None

    # Validator to allow string version of enum value too
    _validate_current_status = validator('current_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)


# CRMLead Update Schema
class CRMLeadUpdateSchema(BaseModel):
    plot_id: int
    customer_id: int
    assigned_so_id: int
    initial_contact_date: Optional[str]
    current_status: Optional[PropertyStatus]

    def get_initial_contact_date(self):
        if self.initial_contact_date:
            try:
                time_obj = datetime.strptime(self.initial_contact_date, '%Y-%m-%dT%H:%M:%SZ')
                return time_obj
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return None

    # Validator to allow string version of enum value too
    _validate_current_status = validator('current_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)


# CRMLead Listing Schema
class CRMLeadListSchema(BaseModel):
    plot_id: Optional[int]
    customer_id: Optional[int]
    assigned_so_id: Optional[int]
    current_status: Optional[PropertyStatus]

    # Validator to allow string version of enum value too
    _validate_current_status = validator('current_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)


# StatusChangeRequest Creation Schema
class StatusChangeRequestCreateSchema(BaseModel):
    crm_lead_id: int
    requested_by_id: int
    approved_by_id: Optional[int]
    requested_status: PropertyStatus
    approval_status: Optional[ApprovalStatus]
    date_requested: Optional[datetime]
    date_approved_rejected: Optional[datetime]

    @validator('date_requested', pre=True, allow_reuse=True)
    def validate_date_requested(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    @validator('date_approved_rejected', pre=True, allow_reuse=True)
    def validate_date_approved_rejected(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_approval_status = validator('approval_status',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_requested_status = validator('requested_status',
                                           allow_reuse=True,
                                           pre=True)(allow_string_rep_of_enum)


# StatusChangeRequest Update Schema
class StatusChangeRequestUpdateSchema(BaseModel):
    crm_lead_id: int
    requested_by_id: int
    approved_by_id: Optional[int]
    requested_status: PropertyStatus
    approval_status: Optional[ApprovalStatus]
    date_requested: Optional[datetime]
    date_approved_rejected: Optional[datetime]

    @validator('date_requested', pre=True, allow_reuse=True)
    def validate_date_requested(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    @validator('date_approved_rejected', pre=True, allow_reuse=True)
    def validate_date_approved_rejected(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_approval_status = validator('approval_status',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_requested_status = validator('requested_status',
                                           allow_reuse=True,
                                           pre=True)(allow_string_rep_of_enum)


# StatusChangeRequest Listing Schema
class StatusChangeRequestListSchema(BaseModel):
    crm_lead_id: Optional[int]
    requested_by_id: Optional[int]
    approved_by_id: Optional[int]
    requested_status: Optional[PropertyStatus]
    approval_status: Optional[ApprovalStatus]
    date_requested: Optional[datetime]
    date_approved_rejected: Optional[datetime]

    @validator('date_requested', pre=True, allow_reuse=True)
    def validate_date_requested(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    @validator('date_approved_rejected', pre=True, allow_reuse=True)
    def validate_date_approved_rejected(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_approval_status = validator('approval_status',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_requested_status = validator('requested_status',
                                           allow_reuse=True,
                                           pre=True)(allow_string_rep_of_enum)


# Payment Creation Schema
class PaymentCreateSchema(BaseModel):
    crm_lead_id: int
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    payment_mode: PaymentMode
    payment_status: Optional[PaymentStatus]
    payment_date: Optional[datetime]
    payment_for: PaymentFor
    payment_detail: Optional[str]
    reference_number: Optional[str]

    @validator('payment_date', pre=True, allow_reuse=True)
    def validate_payment_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_payment_mode = validator('payment_mode',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_status = validator('payment_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_for = validator('payment_for',
                                      allow_reuse=True,
                                      pre=True)(allow_string_rep_of_enum)

    _validate_amount = validator('amount',
                                 allow_reuse=True,
                                 pre=True)(convert_to_decimal)


# Payment Update Schema
class PaymentUpdateSchema(BaseModel):
    crm_lead_id: int
    amount: condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))
    payment_mode: PaymentMode
    payment_status: Optional[PaymentStatus]
    payment_date: Optional[datetime]
    payment_for: PaymentFor
    payment_detail: Optional[str]
    reference_number: Optional[str]

    @validator('payment_date', pre=True, allow_reuse=True)
    def validate_payment_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_payment_mode = validator('payment_mode',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_status = validator('payment_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_for = validator('payment_for',
                                      allow_reuse=True,
                                      pre=True)(allow_string_rep_of_enum)
    _validate_amount = validator('amount',
                                 allow_reuse=True,
                                 pre=True)(convert_to_decimal)


# Payment Listing Schema
class PaymentListSchema(BaseModel):
    crm_lead_id: Optional[int]
    payment_mode: Optional[PaymentMode]
    payment_status: Optional[PaymentStatus]
    payment_for: Optional[PaymentFor]
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    @validator('start_time', pre=True, allow_reuse=True)
    def validate_start_time(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    @validator('end_time', pre=True, allow_reuse=True)
    def validate_end_time(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v

    # Validator to allow string version of enum value too
    _validate_payment_mode = validator('payment_mode',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_status = validator('payment_status',
                                         allow_reuse=True,
                                         pre=True)(allow_string_rep_of_enum)
    # Validator to allow string version of enum value too
    _validate_payment_for = validator('payment_for',
                                      allow_reuse=True,
                                      pre=True)(allow_string_rep_of_enum)


# SiteVisit Creation Schema
class SiteVisitCreateSchema(BaseModel):
    crm_lead_id: int
    is_pickup: bool
    pickup_address: Optional[str]
    pickup_date: Optional[datetime]
    is_drop: bool
    drop_address: Optional[str]
    feedback: Optional[str]

    @validator('pickup_date', pre=True, allow_reuse=True)
    def validate_pickup_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v


# SiteVisit Update Schema
class SiteVisitUpdateSchema(BaseModel):
    crm_lead_id: int
    is_pickup: bool
    pickup_address: Optional[str]
    pickup_date: Optional[datetime]
    is_drop: bool
    drop_address: Optional[str]
    feedback: Optional[str]

    @validator('pickup_date', pre=True, allow_reuse=True)
    def validate_pickup_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v


# SiteVisit List Schema
class SiteVisitListSchema(BaseModel):
    crm_lead_id: Optional[int]
    is_pickup: Optional[bool]
    pickup_date: Optional[datetime]
    is_drop: Optional[bool]

    @validator('pickup_date', pre=True, allow_reuse=True)
    def validate_pickup_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"time format is incorrect: {e}")
        return v
