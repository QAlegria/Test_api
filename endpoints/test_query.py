from typing import Optional

import pytest
import random
import requests
from faker import Faker

from tests.db_tests import QueryUsers


class GetQuery:
    def __init__(self):
        self.status = None
        self.users = None
        self.url = "http://192.168.1.4:5000/users"

    def get_query(self):
        self.status = None
        self.users = None
        response = requests.get(
            f'{self.url}',
            headers={'Content-type': 'application/json'}
        )
        self.users = response.json()
        self.status = response.status_code
        print(f"This is users:   {self.users}")
        print(f"{self.status}")
        return response

    def check_response(self, user_dict):
        print(f"Check response for this user_dict:  {user_dict}")
        check_user_dict = {key: value for key, value in user_dict.items()
                           if value is not None}
        assert any(all(user.get(key) == value for key, value in check_user_dict.items())
                   for user in self.users)

    def check_response_with_deleted_user(self, user_dict):
        print(f"Check response with deleted user for this user_dict:  {user_dict}")
        check_user_dict = {key: value for key, value in user_dict.items()
                           if value is not None}
        assert not any(all(user.get(key) == value for key, value in check_user_dict.items())
                   for user in self.users)

    def check_response_status(self):
        assert self.status == 200

    def find_user(self, user_dict):
        print(f"Looking for this user with the user_dict:  {user_dict}")
        check_user_dict = {key: value for key, value in user_dict.items()
                           if value is not None}
        matching_users = [
            user for user in self.users
            if all(user.get(key) == value for key, value in check_user_dict.items())
        ]
        print(f"Dict with the founded user:  {matching_users}")
        return matching_users

    def check_one_user_with_db_and_query(self, get_user_dictionary: dict):
        db_query = QueryUsers()
        sql_result = db_query.reset_query().filter_dict(get_user_dictionary).constructor_query()
        get_filter_resul = self.find_user(get_user_dictionary)
        print(f"This is response from DB: {sql_result}")
        assert get_filter_resul == sql_result






class PostQuery:
    def __init__(self):
        self.created_user = None
        self.status = None
        self.user_email = None
        self.user_name = None
        self.url = "http://192.168.1.4:5000/users"

    def create_new_user(self, user_name: str = None, user_email: str = None):
        fake = Faker()
        self.user_name = user_name or fake.name()
        self.user_email = user_email or fake.email()
        response = requests.post(
            f'{self.url}',
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




class PutQuery:
    def __init__(self):
        self.user_id = None
        self.changed_user = None
        self.status = None
        self.user_email = None
        self.user_name = None
        self.url = "http://192.168.1.4:5000/users/"

    def change_the_user_params(self, user_dict: dict, user_name: str = None, user_email: str = None,
                               use_fake: bool = True):
        self.user_id = user_dict["id"]
        print(user_dict["id"])
        if use_fake:
            fake = Faker()
            self.user_name = user_name or fake.name()
            self.user_email = user_email or fake.email()
        else:
            self.user_name = user_name
            self.user_email = user_email

        json_data = {
            key: value
            for key, value in [("name", self.user_name), ("email", self.user_email)]
            if value is not None
        }
        response = requests.put(
            f'{self.url}{user_dict["id"]}',
            headers={'Content-type': 'application/json'},
            json=json_data
        )
        self.status = response.status_code
        self.changed_user = response.json()
        return response

    def check_response_status(self):
        assert self.status == 200

    def check_changed_user(self):
        # print(self.user_name, self.user_email, self.user_id)
        assert self.changed_user["id"] == self.user_id
        if self.user_name is None:
            assert self.user_name == self.changed_user["name"]
        if self.user_email is None:
            assert self.user_email == self.changed_user["email"]




class DeleteQuery:
    def __init__(self):
        self.status = None
        self.deleted_user = None
        self.user_dict = None
        self.message = "User deleted"
        self.url = "http://192.168.1.4:5000/users/"

    def delete_user(self, user_dict: dict):
        user_id = user_dict["id"]
        response = requests.delete(
            f'{self.url}{user_id}',
            headers={'Content-type': 'application/json'})
        self.user_dict = user_dict
        self.status = response.status_code
        self.deleted_user = response.json()
        return response

    def check_response_status(self):
        assert self.status == 200

    def check_deleted_user_message(self):
        assert self.deleted_user["message"] == self.message
