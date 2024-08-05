import pytest
from http import HTTPStatus
from helpers import *
from data import *
import allure


class TestOrdersGet:
    @allure.title('Проверка получения списка заказов авторизованным пользователем')
    @allure.description('Тест проверяет, что авторизованный пользователь может получить свой список заказов, '
                        'возвращается код 200')
    def test_get_orders_login_user(self):
        payload_create = create_registration_payload()
        Requests.requests_post_create_user(payload_create)
        response_login = Requests.requests_post_login_user(payload_create)
        token = {'Authorization': response_login.json()["accessToken"]}
        response_ingredients = Requests.requests_get_ingredients()
        payload_create_order = {"ingredients": [response_ingredients.json()["data"][0]["_id"],
                                                response_ingredients.json()["data"][2]["_id"]]}
        Requests.requests_post_create_order(payload_create_order, token)

        response = Requests.requests_get_orders(token)

        assert response.status_code == HTTPStatus.OK

    @allure.title('Проверка получения списка заказов неавторизованным пользователем')
    @allure.description('Тест проверяет, что неавторизованный пользователь не может получить свой список заказов, '
                        'возвращается код 401 и ошибка в теле ответа')
    def test_get_orders_without_login_user(self):
        payload_create = create_registration_payload()
        Requests.requests_post_create_user(payload_create)
        response_login = Requests.requests_post_login_user(payload_create)
        token = {'Authorization': response_login.json()["accessToken"]}
        response_ingredients = Requests.requests_get_ingredients()
        payload_create_order = {"ingredients": [response_ingredients.json()["data"][0]["_id"],
                                                response_ingredients.json()["data"][2]["_id"]]}
        Requests.requests_post_create_order(payload_create_order, token)

        response = Requests.requests_get_orders("")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()["message"] == MESSAGE_4
