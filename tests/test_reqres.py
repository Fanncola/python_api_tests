import requests
import pytest


@pytest.fixture(scope='function')
def get_url():
    url = 'https://reqres.in/api'
    return url


def test_get_list_users(get_url):
    page = 2
    total = 12

    response = requests.get(f'{get_url}/users?page={page}')

    assert response.status_code == 200
    assert response.json()['page'] == page
    assert response.json()['total'] == total


def test_single_user(get_url):
    user_id = 2

    response = requests.get(f'{get_url}/users/{user_id}')

    assert response.json()['data']['id'] == user_id
    assert response.status_code == 200


def test_single_user_nof_found(get_url):
    response = requests.get(f'{get_url}/users/404')

    assert response.status_code == 404
    assert response.json() == {}


def test_crete_user(get_url):
    user_name = 'Joe'
    user_job = 'driver'

    response = requests.post(f'{get_url}/users', json={
        "name": user_name,
        "job": user_job
    })

    assert response.status_code == 201
    assert response.json()['name'] == user_name
    assert response.json()['job'] == user_job


def test_put_user(get_url):
    user_id = 2
    user_name = 'Joe'
    user_job = 'driver'

    response = requests.put(f'{get_url}/users/{user_id}', json={
        "name": user_name,
        "job": user_job
    })

    assert response.status_code == 200
    assert response.json()['name'] == user_name
    assert response.json()['job'] == user_job


def test_patch_user(get_url):
    user_id = 2
    user_name = 'Joe'
    user_job = 'driver'

    response = requests.patch(f'{get_url}/users/{user_id}', json={
        "name": user_name,
        "job": user_job
    })

    assert response.status_code == 200
    assert response.json()['name'] == user_name
    assert response.json()['job'] == user_job


def test_delete_user(get_url):
    user_id = 2

    response = requests.delete(f'{get_url}/users/{user_id}')

    assert response.status_code == 204


def test_register_user_successful(get_url):
    user_email = 'eve.holt@reqres.in'
    user_password = 'pistol'

    response = requests.post(f'{get_url}/register', json={
        "email": user_email,
        "password": user_password
    })

    assert response.status_code == 200
    assert response.json()['id'] > 0
    assert response.json()['token'] != ''


def test_register_user_unsuccessful(get_url):
    user_email = 'eve.holt@reqres.in'

    response = requests.post(f'{get_url}/register', json={
        "email": user_email,
    })

    assert response.status_code == 400
    assert response.json() == {"error": "Missing password"}


def test_user_login_successful(get_url):
    user_email = "eve.holt@reqres.in"
    user_password = "cityslicka"

    response = requests.post(f'{get_url}/login', json={
        "email": user_email,
        "password": user_password
    })

    assert response.status_code == 200
    assert response.json()['token'] != ''


def test_user_login_unsuccessful(get_url):
    user_email = "eve.holt@reqres.in"

    response = requests.post(f'{get_url}/login', json={
        "email": user_email
    })

    assert response.status_code == 400
    assert response.json() == {"error": "Missing password"}


def test_delayed_response(get_url):
    delay = 3
    total = 12
    page = 1

    response = requests.get(f'{get_url}/users?delay={delay}')

    assert response.elapsed.total_seconds() <= 5
    assert response.status_code == 200
    assert response.json()['total'] == total
    assert response.json()['page'] == page
