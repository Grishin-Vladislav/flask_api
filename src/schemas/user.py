import re

import pydantic
from typing import Optional


class Name(pydantic.BaseModel):
    name: str

    @pydantic.field_validator('name')
    @classmethod
    def check_name(cls, v: str):
        if len(v) > 50:
            raise ValueError('name is too long')
        return v


class Email(pydantic.BaseModel):
    email: str

    @pydantic.field_validator('email')
    @classmethod
    def check_email(cls, v: str):
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if len(v) > 50 or not re.fullmatch(regex, v):
            raise ValueError('enter valid email')
        return v


class Password(pydantic.BaseModel):
    password: str

    @pydantic.field_validator('password')
    @classmethod
    def check_password(cls, v: str):
        length_of_pass = len(v)
        if length_of_pass < 8:
            raise ValueError('password is too short')
        if length_of_pass > 100:
            raise ValueError('password is too long')
        return v


class CreateUser(Name, Email, Password):
    name: str
    email: str
    password: str


class UpdateUser(Name, Email, Password):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class LoginUser(Email, Password):
    email: str
    password: str
