import allure
import requests

import urls


class OrderMethod:
    @staticmethod
    def get_ingredients_id():
        with allure.step("Получаем идентификаторы ингредиентов"):
            response = requests.get(urls.URL_GET_INGREDIENTS, timeout=urls.REQUEST_TIMEOUT)
            response.raise_for_status()
            ingredients = response.json().get("data")
            assert isinstance(ingredients, list) and ingredients, "Каталог ингредиентов пуст"
            return [item["_id"] for item in ingredients]

    @staticmethod
    def create_order(access_token, ingredient_ids):
        with allure.step("Отправляем запрос на создание заказа"):
            headers = {"Authorization": access_token} if access_token else {}
            return requests.post(
                urls.URL_CREATE_ORDER,
                headers=headers,
                json={"ingredients": ingredient_ids},
                timeout=urls.REQUEST_TIMEOUT,
            )
