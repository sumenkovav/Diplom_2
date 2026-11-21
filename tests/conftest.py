import sys
import os

# Поднимает корень проекта (на 1 уровень выше папки tests) в путь поиска модулей
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import pytest

from generators import generate_user_payload
from methods.order_methods import OrderMethod
from methods.user_methods import UserMethod
from tests.response_checks import assert_auth_response


@pytest.fixture
def user_payload():
    return generate_user_payload()


@pytest.fixture
def register_user(request):
    def register(payload):
        response = UserMethod.create_user(payload)
        if response.ok:
            token = response.json().get("accessToken")
            if token:
                request.addfinalizer(lambda: UserMethod.delete_user(token))
        return response

    return register


@pytest.fixture
def create_user(user_payload, register_user):
    response = register_user(user_payload)
    assert_auth_response(response, user_payload)
    return {
        "user_data": user_payload,
        "user_data_for_login": {
            "email": user_payload["email"],
            "password": user_payload["password"],
        },
        "access_token": response.json()["accessToken"],
    }


@pytest.fixture
def order_ingredients():
    return OrderMethod.get_ingredients_id()[:3]
