import allure

from data import UserMessageMistake
from generators import generate_unique_email
from methods.user_methods import UserMethod
from response_checks import assert_api_error, assert_auth_response


@allure.sub_suite("Вход пользователя")
class TestUserLogin:
    @allure.title("Вход под существующим пользователем")
    def test_success_login_user(self, create_user):
        response = UserMethod.login_user(create_user["user_data_for_login"])
        assert_auth_response(response, create_user["user_data"])

    @allure.title("Вход с неверным email отклоняется")
    def test_cannot_login_with_invalid_email(self, create_user):
        credentials = create_user["user_data_for_login"].copy()
        credentials["email"] = generate_unique_email()
        response = UserMethod.login_user(credentials)
        assert_api_error(response, 401, UserMessageMistake.INCORRECT_CREDENTIALS)

    @allure.title("Вход с неверным паролем отклоняется")
    def test_cannot_login_with_invalid_password(self, create_user):
        credentials = create_user["user_data_for_login"].copy()
        credentials["password"] += "-incorrect"
        response = UserMethod.login_user(credentials)
        assert_api_error(response, 401, UserMessageMistake.INCORRECT_CREDENTIALS)

    @allure.title("Вход с неверными email и паролем отклоняется")
    def test_cannot_login_with_invalid_email_and_password(self, create_user):
        credentials = create_user["user_data_for_login"].copy()
        credentials["email"] = generate_unique_email()
        credentials["password"] += "-incorrect"
        response = UserMethod.login_user(credentials)
        assert_api_error(response, 401, UserMessageMistake.INCORRECT_CREDENTIALS)
