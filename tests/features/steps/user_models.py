from pydantic import BaseModel


class UserRegister(BaseModel):
    phone_number: str
    password: str
    email: str
    first_name: str


class UserLogin(BaseModel):
    phone_number: str
    password: str

