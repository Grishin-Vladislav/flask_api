from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, jsonify
from flask_scrypt import (generate_password_hash,
                          generate_random_salt,
                          check_password_hash)
from jwt import DecodeError

from config import JWT_SECRET
from src.models import User
from src.tools import get_user_by_email


def hash_password(raw_password) -> dict:
    salt = generate_random_salt().decode()
    password = generate_password_hash(raw_password, salt).decode()
    return {'salt': salt, 'password': password}


def check_password(password, hash, salt) -> bool:
    return check_password_hash(password.encode(), hash.encode(), salt.encode())


def give_jwt(user: User):
    payload = {
        'user': user.dict,
        'exp': datetime.utcnow() + timedelta(minutes=10)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return token


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization').replace('Bearer ', '')
        except AttributeError:
            return jsonify({'response': 'no token provided'}), 401
        except ValueError:
            return jsonify({'response': 'invalid token'}), 401
        if not token:
            return jsonify({'response': 'no token provided'}), 401

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except DecodeError:
            return jsonify({'response': 'invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'response': 'token expired'}), 401

        user = get_user_by_email(payload['user']['email'])

        return f(*args, **kwargs, user=user)

    return wrapper
