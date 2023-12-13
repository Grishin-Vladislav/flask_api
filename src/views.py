from flask import request, jsonify
from flask.views import MethodView

from models import User, Advert
from src import permissions
from src.schemas.advert import CreateAdvert, UpdateAdvert
from src.schemas.user import CreateUser, UpdateUser, LoginUser
from tools import validate, get_user, add_user, \
    get_user_by_email, get_advert, add_advert
from auth import check_password, hash_password, give_jwt, token_required


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
        return jsonify({'success': 'user has been created'}), 201

    @token_required
    def patch(self, user):
        user_data: dict = validate(UpdateUser, request.json)
        for key, value in user_data.items():
            setattr(user, key, value)
        add_user(user)
        return jsonify({'success': 'user has been updated'}), 201

    @token_required
    def delete(self, user):
        self.session.delete(user)
        self.session.commit()
        return jsonify({'success': 'user has been deleted'}), 200


class LoginView(AbstractView):

    def post(self):
        request_data = validate(LoginUser, request.json)
        user: User = get_user_by_email(request_data['email'])
        if check_password(request_data['password'], user.password, user.salt):
            token = give_jwt(user)
            return {'access-token': f'{token}'}, 200
        return jsonify({'response': 'credentials are not correct!'}), 401


class AdvertView(AbstractView):

    def get(self, advert_id):
        advert = get_advert(advert_id)
        return jsonify(advert.dict)

    @token_required
    def post(self, user):
        advert_data: dict = validate(CreateAdvert, request.json)
        advert = Advert(**advert_data, author_id=user.id)
        add_advert(advert)
        return jsonify({'success': 'advert has been created'}), 201

    @token_required
    @permissions.advert_ownership
    def patch(self, advert_id, user, advert):
        # todo: remove unused args
        advert_data = validate(UpdateAdvert, request.json)
        for key, value in advert_data.items():
            setattr(advert, key, value)
        add_advert(advert)
        return jsonify({'success': 'advert has been updated'}), 201

    @token_required
    @permissions.advert_ownership
    def delete(self, advert_id, user, advert):
        # todo: remove unused args
        self.session.delete(advert)
        self.session.commit()
        return jsonify({'success': 'advert has been deleted'}), 200
