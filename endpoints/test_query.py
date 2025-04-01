from typing import Optional

import pytest
import random
import requests
from faker import Faker


class GetQuery:
    def __init__(self):
        self.status = None
        self.users = None

    def get_query(self):
        response = requests.get(
            'http://192.168.1.4:5000/users',
            headers={'Content-type': 'application/json'}
        )
        self.users = response.json()
        self.status = response.status_code
        return response

    def check_response(self, test_dict):
        check_user_dict = {arg_1: arg_2 for arg_1, arg_2 in test_dict.items()
                           if arg_2 is not None}
        assert any(all(user.get(key) == value for key, value in check_user_dict.items())
                   for user in self.users)

    def check_response_status(self, status):
        assert self.status == 200

class PostQuery:
    def __init__(self):
        self.created_user = None
        self.status = None
        self.user_email = None
        self.user_name = None

    def create_new_user(self, user_name: str = None, user_email: str = None):
        fake = Faker()
        self.user_name = user_name or fake.name()
        self.user_email = user_email or fake.email()
        response = requests.post(
            'http://192.168.1.4:5000/users',
            headers={'Content-type': 'application/json'},
            json={'name': self.user_name, 'email': self.user_email}
        )
        self.status = response.status_code
        self.created_user = response.json()
        return response

    def check_response_status(self):
        assert self.status == 201

    def check_created_user(self):
        assert self.created_user["id"] is not None
        assert self.user_name == self.created_user["name"]
        assert self.user_email == self.created_user["email"]