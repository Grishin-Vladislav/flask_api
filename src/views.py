from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from errors import HttpError
from models import User, Advert
from src.schemas.advert import CreateAdvert, UpdateAdvert
from src.schemas.user import CreateUser, UpdateUser, LoginUser
from tools import validate, hash_password, check_password


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


class AbstractView(MethodView):
    @property
    def session(self):
        return request.session


class UserView(AbstractView):

    def get(self, user_id):
        user: User = get_user(user_id)
        return jsonify(user.dict)

    def post(self):
        user_data: dict = validate(CreateUser, request.json)
        secrets = hash_password(user_data['password'])
        user_data['password'] = secrets['password']
        user_data['salt'] = secrets['salt']
        user: User = User(**user_data)
        add_user(user)
        return {'success': 'user has been created'}, 201

    def patch(self, user_id):
        user: User = get_user(user_id)
        user_data: dict = validate(UpdateUser, request.json)
        for key, value in user_data.items():
            setattr(user, key, value)
        add_user(user)
        return {'success': 'user has been updated'}, 201

    def delete(self, user_id):
        user: User = get_user(user_id)
        self.session.delete(user)
        self.session.commit()
        return {'success': 'user has been deleted'}, 200


class LoginView(AbstractView):

    def post(self):
        request_data = validate(LoginUser, request.json)
        user: User = get_user_by_email(request_data['email'])
        if check_password(request_data['password'], user.password, user.salt):
            return {'response': 'credentials correct!'}, 200
        return {'response': 'credentials are not correct!'}, 409


class AdvertView(AbstractView):

    def get(self, advert_id):
        advert = get_advert(advert_id)
        return jsonify(advert.dict)

    def post(self):
        advert_data: dict = validate(CreateAdvert, request.json)
        advert = Advert(**advert_data, author_id=1)  # TODO: get current user
        add_advert(advert)
        return {'success': 'advert has been created'}, 201

    def patch(self, advert_id):
        advert = get_advert(advert_id)
        advert_data = validate(UpdateAdvert, request.json)
        for key, value in advert_data.items():
            setattr(advert, key, value)
        add_advert(advert)
        return {'success': 'advert has been updated'}, 201

    def delete(self, advert_id):
        advert = get_advert(advert_id)
        self.session.delete(advert)
        self.session.commit()
        return {'success': 'advert has been deleted'}, 200
