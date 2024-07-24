import pytest
from http import HTTPStatus
from helpers import *
from data import *
import allure


class TestOrderCreation:
    @allure.title('Проверка успешного создания заказа авторизованным пользователем с указанием ингредиентов')
    @allure.description('Тест проверяет, что авторизованный пользователь может создать заказ, указав ингредиенты, '
                        'возвращается код 200')
    def test_create_order_with_login_and_ingredients(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response_login = Requests.requests_post_login_user(payload)
        token = {'Authorization': response_login.json()["accessToken"]}
        response_ingredients = Requests.requests_get_ingredients()
        payload_create_order = {"ingredients": [response_ingredients.json()["data"][0]["_id"],
                                                response_ingredients.json()["data"][2]["_id"]]}

        response = Requests.requests_post_create_order(payload_create_order, token)

        assert response.status_code == HTTPStatus.OK

    @allure.title('Проверка создания заказа авторизованным пользователем без указания ингредиентов')
    @allure.description('Тест проверяет, что авторизованный пользователь не может создать заказ не указав ингредиенты, '
                        'возвращается код 400 и ошибка в теле ответа')
    def test_create_order_with_login_and_without_ingredients(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response_login = Requests.requests_post_login_user(payload)
        token = {'Authorization': response_login.json()["accessToken"]}

        response = Requests.requests_post_create_order("", token)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == MESSAGE_5

    @allure.title('Проверка создания заказа авторизованным пользователем с некорректными ингредиентами')
    @allure.description('Тест проверяет, что авторизованный пользователь не может создать заказ с некорректными '
                        'ингредиентами, возвращается код 500')
    def test_create_order_with_login_and_incorrect_ingredients(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        response_login = Requests.requests_post_login_user(payload)
        token = {'Authorization': response_login.json()["accessToken"]}
        payload_create_order = {"ingredients": [INCORRECT_INGREDIENT_1, INCORRECT_INGREDIENT_2]}

        response = Requests.requests_post_create_order(payload_create_order, token)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    @allure.title('Проверка создания заказа неавторизованным пользователем')
    @allure.description('Тест проверяет, что неавторизованный пользователь может создать заказ, возвращается код 200')
    def test_create_order_without_login(self):
        payload = create_registration_payload()
        Requests.requests_post_create_user(payload)
        Requests.requests_post_login_user(payload)
        response_ingredients = Requests.requests_get_ingredients()
        payload_create_order = {"ingredients": [response_ingredients.json()["data"][0]["_id"],
                                                response_ingredients.json()["data"][2]["_id"]]}

        response = Requests.requests_post_create_order(payload_create_order, "")

        assert response.status_code == HTTPStatus.OK
