import allure


def assert_auth_response(response, expected_user):
    with allure.step("Проверяем успешный ответ и данные пользователя"):
        assert response.status_code == 200, f"Получен HTTP {response.status_code}"
        body = response.json()
        assert body["success"] is True, "Операция завершилась без признака успеха"
        assert body["user"]["email"] == expected_user["email"], "Email пользователя отличается"
        assert body["user"]["name"] == expected_user["name"], "Имя пользователя отличается"

    with allure.step("Проверяем наличие токенов"):
        access_token = body.get("accessToken")
        refresh_token = body.get("refreshToken")
        has_access_token = (
            isinstance(access_token, str)
            and access_token.startswith("Bearer ")
            and len(access_token) > len("Bearer ")
        )
        has_refresh_token = isinstance(refresh_token, str) and bool(refresh_token)
        assert has_access_token, "В ответе отсутствует токен Bearer"
        assert has_refresh_token, "В ответе отсутствует refreshToken"


def assert_api_error(response, expected_status, expected_error):
    with allure.step(f"Проверяем HTTP {expected_status} и тело ошибки"):
        assert response.status_code == expected_status, f"Получен HTTP {response.status_code}"
        matches_expected_error = response.json() == expected_error
        assert matches_expected_error, f"Ожидалось тело ошибки {expected_error!r}"


def assert_order_created(response):
    with allure.step("Проверяем успешное создание заказа и его номер"):
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["name"], str) and body["name"].strip()
        order_number = body["order"]["number"]
        assert type(order_number) is int and order_number > 0
