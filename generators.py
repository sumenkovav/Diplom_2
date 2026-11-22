from uuid import uuid4

from faker import Faker


fake = Faker()


def generate_unique_email():
    return f"qa-{uuid4().hex}@example.com"


def generate_user_payload():
    return {
        "email": generate_unique_email(),
        "password": fake.password(),
        "name": fake.first_name(),
    }
