import flask
from flask import request, jsonify

from errors import HttpError
from models import Session
from views import UserView, LoginView, AdvertView

app = flask.Flask(__name__)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(404)
def not_found(err):
    return {'description': 'url not found'}, 404


# todo: add 405 method not allowed


@app.errorhandler(500)
def internal(err):
    return {'description': 'internal server error'}, 500


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.description})
    response.status_code = error.status_code
    return response


user_view = UserView.as_view('user_view')
app.add_url_rule('/users/<int:user_id>',
                 view_func=user_view, methods=['GET'])
app.add_url_rule('/users',
                 view_func=user_view, methods=['POST', 'PATCH', 'DELETE'])
app.add_url_rule('/login',
                 view_func=LoginView.as_view('login_view'), methods=['POST'])

advert_view = AdvertView.as_view('advert_view')
app.add_url_rule('/adverts/<int:advert_id>', view_func=advert_view,
                 methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/adverts',
                 view_func=advert_view, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
