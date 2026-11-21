import allure

from data import INVALID_INGREDIENTS, OrderMessageMistake
from methods.order_methods import OrderMethod
from tests.response_checks import assert_api_error


def assert_order_created(response):
    with allure.step("Проверяем успешное создание заказа и его номер"):
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["name"], str) and body["name"].strip()
        order_number = body["order"]["number"]
        assert type(order_number) is int and order_number > 0


@allure.sub_suite("Создание заказа")
class TestOrderCreate:
    @allure.title("Заказ с ингредиентами от авторизованного пользователя")
    def test_create_order_login_user_with_ingredients(self, create_user, order_ingredients):
        response = OrderMethod.create_order(create_user["access_token"], order_ingredients)
        assert_order_created(response)

    @allure.title("Заказ с ингредиентами без авторизации")
    @allure.description("Учебный стенд принимает заказ с ингредиентами без заголовка Authorization")
    def test_create_order_user_without_login_with_ingredients(self, order_ingredients):
        response = OrderMethod.create_order(None, order_ingredients)
        assert_order_created(response)

    @allure.title("Заказ без ингредиентов с авторизацией отклоняется")
    def test_not_create_order_login_user_without_ingredients(self, create_user):
        response = OrderMethod.create_order(create_user["access_token"], [])
        assert_api_error(response, 400, OrderMessageMistake.NO_INGREDIENTS_ERROR)

    @allure.title("Заказ без ингредиентов и без авторизации отклоняется")
    def test_not_create_order_without_login_without_ingredients(self):
        response = OrderMethod.create_order(None, [])
        assert_api_error(response, 400, OrderMessageMistake.NO_INGREDIENTS_ERROR)

    @allure.title("При неверном хеше ингредиента API возвращает HTTP 500")
    def test_not_create_order_login_user_with_error_ingredients(self, create_user):
        response = OrderMethod.create_order(create_user["access_token"], INVALID_INGREDIENTS)
        with allure.step("Проверяем HTTP 500 по документации API"):
            assert response.status_code == 500
