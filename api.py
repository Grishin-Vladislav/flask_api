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


def patch_user(user_id, **kwargs):
    response = requests.patch(
        base_url + f'users/{user_id}',
        json=kwargs
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
    log(response)
