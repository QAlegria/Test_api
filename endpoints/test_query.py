from typing import Optional

import pytest
import random
import requests

class GetQuery:
    def __init__(self):
        self.users = None

    def get_query(self):
        response = requests.get(
            'http://192.168.1.4:5000/users',
            headers={'Content-type': 'application/json'}
        )
        self.users = response.json()
        return response

    def check_response(self, test_dict):
        check_user_dict = {arg_1: arg_2 for arg_1, arg_2 in test_dict.items()
                           if arg_2 is not None}
        assert any(all(user.get(key) == value for key, value in check_user_dict.items())
                   for user in self.users)
