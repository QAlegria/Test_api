import pytest
import requests
import random
from faker import Faker
from db_tests import QueryUsers

fake = Faker()
db_query = QueryUsers()

@pytest.fixture()
def get_random_id():
    response = requests.get(
        'http://192.168.1.4:5000/users',
        headers={'Content-type': 'application/json'}
    )
    users = response.json()
    ids = sorted(list(map(lambda user: user["id"], users)))
    user_id = ids[random.randint(1,len(ids)-1)]
    return user_id

def test_get_request():
    response = requests.get(
        'http://192.168.1.4:5000/users',
        headers={'Content-type': 'application/json'}
    )
    users = response.json()
    user_id = 1
    email = 'test@test.test'
    sql_query = db_query.filter_by_id(user_id).filter_by_email(email).constructor_query()
    assert any(user["id"] == user_id and user["email"] == email for user in sql_query)
    assert response.status_code == 200
    assert any(user["id"] == user_id and user["email"] == email for user in users)

def test_post_request():

    fake_name = fake.name()
    fake_email = fake.email()
    response = requests.post(
        'http://192.168.1.4:5000/users',
        headers={'Content-type': 'application/json'},
        json={'name': fake_name, 'email': fake_email}
    )
    assert response.status_code == 201

def test_put_request(get_random_id):
    fake_name = fake.name()
    fake_email = fake.email()
    response = requests.put(
        f'http://192.168.1.4:5000/users/{get_random_id}',
        headers={'Content-type': 'application/json'},
        json={'name': fake_name, 'email': fake_email}
    )
    assert response.status_code == 200

def test_delete_request(get_random_id):
    response = requests.delete(
        f'http://192.168.1.4:5000/users/{get_random_id}',
        headers={'Content-type': 'application/json'})
    assert response.status_code == 200