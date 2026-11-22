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


@pytest.fixture
def user_payload():
    return generate_user_payload()


@pytest.fixture
def cleanup_users(request):
    scheduled_tokens = set()

    def schedule_deletion(response):
        if not response.ok:
            return

        token = response.json().get("accessToken")
        if token and token not in scheduled_tokens:
            scheduled_tokens.add(token)
            request.addfinalizer(lambda: UserMethod.delete_user(token))

    return schedule_deletion


@pytest.fixture
def create_user(user_payload, cleanup_users):
    response = UserMethod.create_user(user_payload)
    cleanup_users(response)
    response.raise_for_status()
    access_token = response.json().get("accessToken")
    if not access_token:
        raise RuntimeError("Для тестового пользователя не получен accessToken")
    return {
        "user_data": user_payload,
        "user_data_for_login": {
            "email": user_payload["email"],
            "password": user_payload["password"],
        },
        "access_token": access_token,
    }


@pytest.fixture
def order_ingredients():
    return OrderMethod.get_ingredients_id()[:3]
