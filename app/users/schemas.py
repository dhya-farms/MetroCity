from typing import Optional, List

from pydantic.v1 import BaseModel, validator

from app.users.enums import Role
from datetime import datetime

from app.utils.helpers import trim_mobile_no, allow_string_rep_of_enum


# User Creation Schema
class UserCreateSchema(BaseModel):
    name: str
    email: str
    mobile_no: str
    role: Role
    director_id: Optional[int]

    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)

    # Validator to allow string version of enum value too
    _validate_role = validator('role',
                               allow_reuse=True,
                               pre=True)(allow_string_rep_of_enum)


# User Update Schema
class UserUpdateSchema(BaseModel):
    name: str
    email: str
    mobile_no: str
    role: Role
    director_id: Optional[int]

    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)

    # Validator to allow string version of enum value too
    _validate_role = validator('role',
                               allow_reuse=True,
                               pre=True)(allow_string_rep_of_enum)


# User Listing Schema
class UserListSchema(BaseModel):
    username: Optional[str]
    name: Optional[str]
    email: Optional[str]
    mobile_no: Optional[str]
    role: Optional[Role]
    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)

    # Validator to allow string version of enum value too
    _validate_role = validator('role',
                               allow_reuse=True,
                               pre=True)(allow_string_rep_of_enum)


# Customer Creation Schema
class CustomerCreateSchema(BaseModel):
    name: str
    email: Optional[str]
    mobile_no: str
    occupation: str
    address: str
    preferences: Optional[dict]
    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)


# Customer Update Schema
class CustomerUpdateSchema(BaseModel):
    name: str
    email: Optional[str]
    mobile_no: Optional[str]
    occupation: str
    address: str
    preferences: Optional[dict]
    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)


# Customer Listing Schema
class CustomerListSchema(BaseModel):
    user_id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    mobile_no: Optional[str]
    # validator to trim  display number
    _validate_mobile_no = validator('mobile_no',
                                    allow_reuse=True,
                                    pre=True)(trim_mobile_no)
