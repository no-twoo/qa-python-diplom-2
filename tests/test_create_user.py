import pytest
from http import HTTPStatus
from helpers import *
from data import *
import allure


class TestUserCreation:
    @allure.title('Проверка успешного создания пользователя')
    @allure.description('Тест проверяет, что при успешном создании пользователя возвращается код 200')
    def test_create_user_successful(self):
        payload = create_registration_payload()
        response = Requests.requests_post_create_user(payload)

        assert response.status_code == HTTPStatus.OK

    @allure.title('Проверка, что нельзя создать двух одинаковых пользователей')
    @allure.description('Тест проверяет, что при создании пользователей с одинаковыми данными возвращается код 403 и '
                        'ошибка в теле ответа')
    def test_create_two_identical_users(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response = Requests.requests_post_create_user(payload)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["message"] == MESSAGE_1

    @allure.title('Проверка создания пользователя без email')
    @allure.description('Тест проверяет, что при создании пользователя без email возвращается код 403 и '
                        'ошибка в теле ответа')
    def test_create_user_without_email(self):
        password = generate_random_string(10)
        name = generate_random_string(10)
        payload = {
            "password": password,
            "name": name
        }
        response = Requests.requests_post_create_user(payload)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert response.json()["message"] == MESSAGE_2
