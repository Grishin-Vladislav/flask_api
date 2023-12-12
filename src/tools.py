from pydantic import ValidationError
from flask_scrypt import (generate_password_hash,
                          generate_random_salt,
                          check_password_hash)

from errors import HttpError


def validate(schema_cls, json_data: dict | list):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        error.pop('url', None)
        raise HttpError(400, error)


def hash_password(raw_password) -> dict:
    salt = generate_random_salt().decode()
    password = generate_password_hash(raw_password, salt).decode()
    return {'salt': salt, 'password': password}


def check_password(password, hash, salt) -> bool:
    return check_password_hash(password.encode(), hash.encode(), salt.encode())
