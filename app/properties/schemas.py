import json

from _decimal import Decimal
from django.contrib.auth import get_user_model
from pydantic.v1 import BaseModel, validator, condecimal, constr, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.properties.enums import Facing, SoilType
from app.properties.enums import PropertyType, AreaSizeUnit, AreaOfPurpose, PhaseStatus
from app.properties.enums import Availability
from app.users.models import Customer
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal

User = get_user_model()


class UpdateListSchema(BaseModel):
    pass


# Property Creation Schema
class PropertyCreateSchema(BaseModel):
    property_type: PropertyType
    description: Optional[str]
    area_of_purpose: AreaOfPurpose
    name: str
    details: Optional[Dict[str, Any]] = Field(default_factory=dict)
    location: Optional[str]
    gmap_url: Optional[HttpUrl] = None
    director_id: Optional[int]
    current_lead_id: Optional[int]

    @validator('details', pre=True)
    def parse_details(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError('Invalid JSON format')
        elif not isinstance(v, dict):
            raise TypeError('Details must be a dictionary or a JSON string.')
        return v


    _validate_property_type = validator('property_type',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)

    _validate_area_of_purpose = validator('area_of_purpose',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)


# Property Creation Schema
class PropertyUpdateSchema(PropertyCreateSchema):
    pass


# Property Listing Schema
class PropertyListSchema(BaseModel):
    property_type: Optional[PropertyType]
    area_of_purpose: Optional[AreaOfPurpose]
    created_by_id: Optional[int]
    director_id: Optional[int]
    current_lead_id: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]

    @validator('start_time', pre=True, allow_reuse=True)
    def validate_start_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    # @validator('current_lead_id', pre=True, allow_reuse=True)
    # def convert_customer_id(cls, v):
    #     if v:
    #         user_instance = User.objects.get(id=int(v))
    #         try:
    #             customer_id = user_instance.customer.id  # Accessing the related Customer instance and its ID
    #         except Customer.DoesNotExist:
    #             customer_id = None  # In case the User instance has no related Customer
    #         return customer_id
    #     return v

    @validator('end_time', pre=True, allow_reuse=True)
    def validate_estimated_completion_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"End time format is incorrect: {e}")
        return v

    _validate_property_type = validator('property_type',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)
    _validate_area_of_purpose = validator('area_of_purpose',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)


# Phase Creation Schema
class PhaseCreateSchema(BaseModel):
    property_id: int
    phase_number: int
    description: Optional[str]
    start_date: datetime
    estimated_completion_date: Optional[datetime]
    status: Optional[PhaseStatus]
    # Validator to allow string version of enum value too
    _validate_status = validator('status',
                                 allow_reuse=True,
                                 pre=True)(allow_string_rep_of_enum)

    @validator('start_date', pre=True, allow_reuse=True)
    def validate_start_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    @validator('estimated_completion_date', pre=True, allow_reuse=True)
    def validate_estimated_completion_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"End time format is incorrect: {e}")
        return v


# Phase Update Schema
class PhaseUpdateSchema(BaseModel):
    phase_number: int
    description: Optional[str]
    start_date: datetime
    estimated_completion_date: Optional[datetime]
    status: Optional[PhaseStatus]

    # Validator to allow string version of enum value too
    _validate_status = validator('status',
                                 allow_reuse=True,
                                 pre=True)(allow_string_rep_of_enum)

    @validator('start_date', pre=True, allow_reuse=True)
    def validate_start_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    @validator('estimated_completion_date', pre=True, allow_reuse=True)
    def validate_estimated_completion_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"End time format is incorrect: {e}")
        return v


# Phase Listing Schema
class PhaseListSchema(BaseModel):
    property_id: Optional[int]
    phase_number: Optional[int]
    start_date: Optional[datetime]
    estimated_completion_date: Optional[datetime]
    status: Optional[PhaseStatus]

    _validate_status = validator('status',
                                 allow_reuse=True,
                                 pre=True)(allow_string_rep_of_enum)

    @validator('start_date', pre=True, allow_reuse=True)
    def validate_start_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"Start time format is incorrect: {e}")
        return v

    @validator('estimated_completion_date', pre=True, allow_reuse=True)
    def validate_estimated_completion_date(cls, v):
        if v:
            try:
                return datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError as e:
                raise ValueError(f"End time format is incorrect: {e}")
        return v


# Plot Creation Schema
class PlotCreateSchema(BaseModel):
    phase_id: int
    plot_number: int
    is_corner_site: Optional[bool]
    dimensions: Optional[str]
    facing: Optional[Facing]
    soil_type: Optional[SoilType]
    plantation: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    area_size: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    area_size_unit: AreaSizeUnit = AreaSizeUnit.SQ_FT
    availability: Optional[Availability]

    # Validator to allow string version of enum value too
    _validate_availability = validator('availability',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)
    _validate_facing = validator('facing',
                                 allow_reuse=True,
                                 pre=True)(allow_string_rep_of_enum)
    _validate_soil_type = validator('soil_type',
                                    allow_reuse=True,
                                    pre=True)(allow_string_rep_of_enum)
    _validate_price = validator('price', 'area_size',
                                allow_reuse=True,
                                pre=True)(convert_to_decimal)


# Plot Update Schema
class PlotUpdateSchema(BaseModel):
    phase_id: int
    plot_number: int
    is_corner_site: Optional[bool]
    dimensions: Optional[str]
    facing: Optional[Facing]
    soil_type: Optional[SoilType]
    plantation: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    area_size: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    area_size_unit: AreaSizeUnit
    availability: Optional[Availability]
    is_sold: Optional[bool]

    # Validator to allow string version of enum value too
    _validate_availability = validator('availability',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)
    _validate_facing = validator('facing',
                                 allow_reuse=True,
                                 pre=True)(allow_string_rep_of_enum)
    _validate_soil_type = validator('soil_type',
                                    allow_reuse=True,
                                    pre=True)(allow_string_rep_of_enum)
    _validate_price = validator('price', 'area_size',
                                allow_reuse=True,
                                pre=True)(convert_to_decimal)


# Plot Listing Schema
class PlotListSchema(BaseModel):
    phase_id: Optional[int]
    is_corner_site: Optional[bool]
    availability: Optional[Availability]
    facing: Optional[Facing]
    soil_type: Optional[SoilType]
    is_sold: Optional[bool]

    # Validator to allow string version of enum value too
    _validate_availability = validator('availability',
                                       allow_reuse=True,
                                       pre=True)(allow_string_rep_of_enum)
    _validate_facing = validator('facing',
                                 allow_reuse=True,
                                 pre=True)(allow_string_rep_of_enum)
    _validate_soil_type = validator('soil_type',
                                    allow_reuse=True,
                                    pre=True)(allow_string_rep_of_enum)
