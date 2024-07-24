import pytest
from http import HTTPStatus
from helpers import *
from data import *
import allure


class TestUserUpdate:
    @allure.title('Проверка успешного изменения email авторизованного пользователя')
    @allure.description('Тест проверяет, что авторизованный пользователь может изменить свой email, '
                        'возвращается код 200')
    def test_update_email_with_login(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response_login = Requests.requests_post_login_user(payload)
        token = {'Authorization': response_login.json()["accessToken"]}
        email = f"{generate_random_string(10)}@yandex.ru"
        payload_update = {
            "email": email,
            "password": payload["password"]
        }

        response_update = Requests.requests_patch_update_user(payload_update, token)

        assert response_update.status_code == HTTPStatus.OK

    @allure.title('Проверка успешного изменения пароля авторизованного пользователя')
    @allure.description('Тест проверяет, что авторизованный пользователь может изменить свой пароль, '
                        'возвращается код 200')
    def test_update_password_with_login(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response_login = Requests.requests_post_login_user(payload)
        token = {'Authorization': response_login.json()["accessToken"]}
        payload_update = {
            "email": payload["email"],
            "password": CORRECT_PASSWORD
        }

        response_update = Requests.requests_patch_update_user(payload_update, token)

        assert response_update.status_code == HTTPStatus.OK

    @allure.title('Проверка успешного изменения имени авторизованного пользователя')
    @allure.description('Тест проверяет, что авторизованный пользователь может изменить своё имя, '
                        'возвращается код 200')
    def test_update_name_with_login(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response_login = Requests.requests_post_login_user(payload)
        token = {'Authorization': response_login.json()["accessToken"]}
        payload_update = {
            "email": payload["email"],
            "password": payload["password"],
            "name": CORRECT_NAME
        }

        response_update = Requests.requests_patch_update_user(payload_update, token)

        assert response_update.status_code == HTTPStatus.OK

    @allure.title('Проверка невозможности изменения данных у неавторизованного пользователя')
    @allure.description('Тест проверяет, что неавторизованный пользователь не может изменить свои данные, '
                        'возвращается код 401 и ошибка в теле ответа')
    def test_update_user_without_login(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        payload_update = {
            "email": payload["email"],
            "password": CORRECT_PASSWORD,
            "name": payload["name"]
        }

        response_update = Requests.requests_patch_update_user(payload_update, "")

        assert response_update.status_code == HTTPStatus.UNAUTHORIZED
        assert response_update.json()["message"] == MESSAGE_4
