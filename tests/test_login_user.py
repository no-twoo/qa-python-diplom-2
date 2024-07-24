import pytest
from http import HTTPStatus
from helpers import *
from data import *
import allure


class TestUserLogin:
    @allure.title('Проверка успешной авторизации пользователя')
    @allure.description('Тест проверяет, что пользователь может авторизоваться, возвращается код 200')
    def test_login_user_successful(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response = Requests.requests_post_login_user(payload)

        assert response.status_code == HTTPStatus.OK

    @allure.title('Проверка авторизации пользователя с некорректным email')
    @allure.description('Тест проверяет, что пользователь не может авторизоваться с некорректным email, возвращается '
                        'код 401 и ошибка в теле ответа')
    def test_login_user_with_incorrect_email(self):
        payload_create_user = create_registration_payload()
        payload_login_user = {
            "email": INCORRECT_EMAIL,
            "password": payload_create_user["password"]
        }
        Requests.requests_post_create_user(payload_create_user)
        response = Requests.requests_post_login_user(payload_login_user)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["message"] == MESSAGE_3

    @allure.title('Проверка авторизации пользователя с некорректным паролем')
    @allure.description('Тест проверяет, что пользователь не может авторизоваться с некорректным паролем, возвращается '
                        'код 401 и ошибка в теле ответа')
    def test_login_user_with_incorrect_password(self):
        payload_create_user = create_registration_payload()
        payload_login_user = {
            "email": payload_create_user["email"],
            "password": INCORRECT_PASSWORD
        }
        Requests.requests_post_create_user(payload_create_user)
        response = Requests.requests_post_login_user(payload_login_user)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["message"] == MESSAGE_3
