from typing import Optional

from pydantic import BaseModel, Field


class UserAuthModel(BaseModel):
    access_token: str
    refresh_token: str
    first_name: str


class UserRegistrationModel(BaseModel):
    phone_number: str
    password: str
    first_name: str
    email: str


class UserProfileModel(BaseModel):
    address: Optional[str]
    isAdmin: bool
    first_name: str
    active: bool
    email: str
    id: int
    phone_number: str


class UserGetModel(BaseModel):
    active: bool
    phone_number: str
    isAdmin: bool
    address: Optional[str]
    first_name: str
    email: str
    id: int


class UserPutModel(BaseModel):
    phone_number: str
    password: str
    first_name: str
    email: str
    address: str

