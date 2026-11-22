import allure
import requests

import urls


class UserMethod:
    @staticmethod
    def create_user(user_payload):
        with allure.step("Регистрируем пользователя"):
            return requests.post(
                urls.URL_CREATE_USER, json=user_payload, timeout=urls.REQUEST_TIMEOUT
            )

    @staticmethod
    def login_user(user_data):
        with allure.step("Выполняем вход"):
            return requests.post(
                urls.URL_LOGIN_USER, json=user_data, timeout=urls.REQUEST_TIMEOUT
            )

    @staticmethod
    def delete_user(access_token):
        with allure.step("Удаляем тестового пользователя"):
            response = requests.delete(
                urls.URL_DELETE_USER,
                headers={"Authorization": access_token},
                timeout=urls.REQUEST_TIMEOUT,
            )
            assert response.ok, f"Удаление пользователя вернуло HTTP {response.status_code}"
   