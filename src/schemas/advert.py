import pydantic
from typing import Optional


class Name(pydantic.BaseModel):
    name: str

    @pydantic.field_validator('name')
    @classmethod
    def check_name(cls, v: str):
        if len(v) > 50:
            raise ValueError('name is too long')
        if len(v) < 3:
            raise ValueError('name is too short')
        return v


class Description(pydantic.BaseModel):
    description: str

    @pydantic.field_validator('description')
    @classmethod
    def check_description(cls, v: str):
        if len(v) > 300:
            raise ValueError('description is too long')
        if len(v) < 3:
            raise ValueError('description is too short')
        return v


class CreateAdvert(Name, Description):
    name: str
    description: str


class UpdateAdvert(Name, Description):
    name: Optional[str] = None
    description: Optional[str] = None
