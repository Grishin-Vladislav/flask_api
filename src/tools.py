from flask import request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from errors import HttpError
from src.models import User, Advert


def validate(schema_cls, json_data: dict | list):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        error.pop('url', None)
        raise HttpError(400, error)


def get_user(user_id: int):
    user: User | None = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def get_advert(advert_id: int):
    advert: Advert | None = request.session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, 'advert not found')
    return advert


def get_user_by_email(email: str):
    user: User | None = request.session.query(User).filter_by(
        email=email).first()
    if user is None:
        raise HttpError(404, 'user not found')
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'user already exists')


def add_advert(advert: Advert):
    try:
        request.session.add(advert)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, 'advert with this name already exists')
