import requests
import random
import string
from data import *


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def create_registration_payload():
    email = f"{generate_random_string(10)}@yandex.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)

    payload = {
        "email": email,
        "password": password,
        "name": name
    }

    return payload


class Requests:
    @staticmethod
    def requests_post_create_user(data):
        return requests.post(f"{TEST_URL}/api/auth/register", data=data)

    @staticmethod
    def requests_post_login_user(data):
        return requests.post(f"{TEST_URL}/api/auth/login", data=data)

    @staticmethod
    def requests_patch_update_user(data, headers):
        return requests.patch(f"{TEST_URL}/api/auth/user", data=data, headers=headers)

    @staticmethod
    def requests_post_create_order(data, headers):
        return requests.post(f"{TEST_URL}/api/orders", data=data, headers=headers)

    @staticmethod
    def requests_get_ingredients():
        return requests.get(f"{TEST_URL}/api/ingredients")

    @staticmethod
    def requests_get_orders(headers):
        return requests.get(f"{TEST_URL}/api/orders", headers=headers)
