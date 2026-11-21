import allure
import pytest

from data import UserMessageMistake
from tests.response_checks import assert_api_error, assert_auth_response


@allure.sub_suite("Создание пользователя")
class TestUserCreate:
    @allure.title("Уникального пользователя можно зарегистрировать")
    def test_success_create_user(self, user_payload, register_user):
        response = register_user(user_payload)
        assert_auth_response(response, user_payload)

    @allure.title("Повторная регистрация пользователя отклоняется")
    def test_duplicate_user_creation_fail(self, create_user, register_user):
        response = register_user(create_user["user_data"])
        assert_api_error(response, 403, UserMessageMistake.DUPLICATE_USER)

    @allure.title("Регистрация без поля {missing_field} отклоняется")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_cannot_create_user_without_required_field(self, user_payload, register_user, missing_field):
        user_data = user_payload.copy()
        user_data.pop(missing_field)
        response = register_user(user_data)
        assert_api_error(response, 403, UserMessageMistake.REQUIRED_FIELD)
