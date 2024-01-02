from _decimal import Decimal
from pydantic.v1 import BaseModel, validator, condecimal
from typing import Optional
from datetime import datetime

from app.properties.enums import Facing, SoilType
from app.properties.enums import PropertyType, AreaSizeUnit, AreaOfPurpose, PhaseStatus
from app.properties.enums import Availability
from app.utils.helpers import allow_string_rep_of_enum, convert_to_decimal


# Property Creation Schema
class PropertyCreateSchema(BaseModel):
    property_type: PropertyType
    area_of_purpose: AreaOfPurpose
    name: str
    dtcp_details: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    amenities: Optional[str]
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
    area_of_purpose: AreaOfPurpose
    name: str
    dtcp_details: Optional[str]
    price: Optional[condecimal(max_digits=10, decimal_places=2, ge=Decimal(0))]
    amenities: Optional[str]
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
