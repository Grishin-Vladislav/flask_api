import time

import requests

base_url = 'http://127.0.0.1:5000/'


def log(response) -> None:
    print(
        f'status-code: {response.status_code}\n'
        f'content:\n{response.json()}'
    )


def get_user(user_id):
    response = requests.get(
        base_url + f'users/{user_id}'
    )
    log(response)


def create_user(name, email, password):
    response = requests.post(
        base_url + 'users',
        json={
            'name': name,
            'email': email,
            'password': password
        }
    )
    log(response)


def patch_user(token, **kwargs):
    response = requests.patch(
        base_url + 'users',
        headers={
            'Authorization': f'Bearer {token}'
        },
        json=kwargs
    )
    log(response)


def delete_user(token):
    response = requests.delete(
        base_url + 'users',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    log(response)


def login_as_user(email, password):
    response = requests.post(
        base_url + f'login',
        json={
            'email': email,
            'password': password
        }
    )
    token = response.json()['access-token']
    log(response)
    return token


def create_advert(token, name, description):
    response = requests.post(
        base_url + 'adverts',
        headers={
            'Authorization': f'Bearer {token}'
        },
        json={
            'name': name,
            'description': description
        }
    )
    log(response)


def get_advert(advert_id):
    response = requests.get(
        base_url + f'adverts/{advert_id}'
    )
    log(response)


def patch_advert(token, advert_id, **kwargs):
    response = requests.patch(
        base_url + f'adverts/{advert_id}',
        headers={
            'Authorization': f'Bearer {token}'
        },
        json=kwargs
    )
    log(response)


def delete_advert(token, advert_id):
    response = requests.delete(
        base_url + f'adverts/{advert_id}',
        headers={
            'Authorization': f'Bearer {token}'
        }
    )
    log(response)
