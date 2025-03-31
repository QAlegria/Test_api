import requests
from faker import Faker

from endpoints.test_query import GetQuery
from tests.db_tests import QueryUsers

fake = Faker()
db_query = QueryUsers()
get_request = GetQuery()


def test_get_request(check_the_first_stable_user, get_response):
    get_request.get_query()
    get_request.check_response(check_the_first_stable_user)
    db_query.filter_dict(check_the_first_stable_user).constructor_query()

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