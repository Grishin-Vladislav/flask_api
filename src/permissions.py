from functools import wraps

from flask import jsonify

from src.tools import get_advert


def advert_ownership(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = kwargs['user']
        advert = get_advert(kwargs['advert_id'])
        if advert.author_id != user.id:
            return jsonify({'response': 'this is not your advert'}), 403

        return f(*args, **kwargs, advert=advert)

    return wrapper
