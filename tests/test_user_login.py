import allure
import pytest

from data import UserMessageMistake
from generators import generate_unique_email
from methods.user_methods import UserMethod
from tests.response_checks import assert_api_error, assert_auth_response


@allure.sub_suite("Вход пользователя")
class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    def test_success_login_user(self, create_user):
        response = UserMethod.login_user(create_user["user_data_for_login"])
        assert_auth_response(response, create_user["user_data"])

    @allure.title("Вход с неверными учётными данными ({param_id})")
    @pytest.mark.parametrize(
        "wrong_fields",
        [
            pytest.param(("email",), id="wrong-email"),
            pytest.param(("password",), id="wrong-password"),
            pytest.param(("email", "password"), id="wrong-email-and-password"),
        ],
    )
    def test_user_cannot_login_with_invalid_credentials(self, create_user, wrong_fields):
        credentials = create_user["user_data_for_login"].copy()
        if "email" in wrong_fields:
            credentials["email"] = generate_unique_email()
        if "password" in wrong_fields:
            credentials["password"] += "-incorrect"
        response = UserMethod.login_user(credentials)
        assert_api_error(response, 401, UserMessageMistake.INCORRECT_CREDENTIALS)
