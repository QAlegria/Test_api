import pytest
import random
import requests

from endpoints.test_query import GetQuery, PostQuery, PutQuery, DeleteQuery
from database.db_functions import QueryUsers


@pytest.fixture()
def get_random_user():
    response = requests.get(
        'http://90.156.135.158:5000/users',
        headers={'Content-type': 'application/json'}
    )
    users = response.json()
    ids = sorted(list(map(lambda user: user["id"], users)))
    user_id = ids[random.randint(1,len(ids)-1)]
    users_gen = (user_dict for user_dict in users if user_dict.get("id") == user_id)
    new_users = next(users_gen, None)
    print(f"This is random user: {new_users}")
    return new_users

@pytest.fixture()
def check_the_first_stable_user():
    return {
        "id": 1,
        "email": "test@test.test"
    }

@pytest.fixture()
def get_response():
    return GetQuery()

@pytest.fixture()
def get_new_user():
    return PostQuery()

@pytest.fixture()
def db_query():
    return QueryUsers()

@pytest.fixture()
def change_user():
    return PutQuery()

@pytest.fixture()
def delete_user():
    return DeleteQuery()