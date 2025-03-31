import pytest
import random
import requests

from endpoints.test_query import GetQuery


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

@pytest.fixture()
def check_the_first_stable_user():
    return {
        "id": 1,
        "email": "test@test.test"
    }

@pytest.fixture()
def get_response():
    return GetQuery()