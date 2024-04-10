from _decimal import Decimal
from django.contrib.auth import get_user_model
from pydantic.v1 import BaseModel, validator, condecimal, constr
from typing import Optional, List
from datetime import datetime

from app.properties.enums import Facing, SoilType
from app.properties.enums import PropertyType, AreaSizeUnit, AreaOfPurpose, PhaseStatus
from app.properties.enums import Availability
from app.users.models import Customer
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal

User = get_user_model()
# Property Creation Schema
class PropertyCreateSchema(BaseModel):
    property_type: PropertyType
    plots_available: Optional[int]
    sq_ft_from: Optional[str]
    description: Optional[str]
    area_of_purpose: AreaOfPurpose
    name: str
    dtcp_details: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    amenities: List[constr(strip_whitespace=True, min_length=1)] = []
    nearby_attractions: List[constr(strip_whitespace=True, min_length=1)] = []
    location: Optional[str]
    phase_number: Optional[int]
    created_by_id: Optional[int]
    director_id: Optional[int]
    current_lead_id: Optional[int]

    _validate_price = validator('price',
                                allow_reuse=True,
                                pre=True)(convert_to_decimal)

    _validate_property_type = validator('property_type',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)

    _validate_area_of_purpose = validator('area_of_purpose',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)


# Property Creation Schema
class PropertyUpdateSchema(BaseModel):
    property_type: PropertyType
    plots_available: Optional[int]
    sq_ft_from: Optional[str]
    description: Optional[str]
    area_of_purpose: AreaOfPurpose
    name: str
    dtcp_details: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    amenities: List[constr(strip_whitespace=True, min_length=1)] = []
    nearby_attractions: List[constr(strip_whitespace=True, min_length=1)] = []
    location: Optional[str]
    phase_number: Optional[int]
    created_by_id: Optional[int]
    director_id: Optional[int]
    current_lead_id: Optional[int]

    _validate_price = validator('price',
                                allow_reuse=True,
                                pre=True)(convert_to_decimal)

    _validate_property_type = validator('property_type',
                                        allow_reuse=True,
                                        pre=True)(allow_string_rep_of_enum)

    _validate_area_of_purpose = validator('area_of_purpose',
                                          allow_reuse=True,
                                          pre=True)(allow_string_rep_of_enum)


# Property Listing Schema
class PropertyListSchema(BaseModel):
    property_type: Optional[PropertyType]
    area_of_purpose: Optional[AreaOfPurpose]
    phase_number: Optional[int]
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
    area_size: int
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
    _validate_price = validator('price',
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
    area_size: int
    area_size_unit: AreaSizeUnit
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
    _validate_price = validator('price',
                                allow_reuse=True,
                                pre=True)(convert_to_decimal)


# Plot Listing Schema
class PlotListSchema(BaseModel):
    phase_id: Optional[int]
    is_corner_site: Optional[bool]
    availability: Optional[Availability]
    facing: Optional[Facing]
    soil_type: Optional[SoilType]

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
