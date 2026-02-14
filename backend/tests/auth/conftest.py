import pytest
from faker import Faker

from backend.src.services.authentication.auth_service import AuthService
from backend.src.services.authentication.helpers.auth_helper import AuthHelper
from backend.src.services.authentication.models.request.login_request import LoginRequest
from backend.src.services.authentication.models.request.register_request import RegisterRequest
from backend.src.utils.api_utils import ApiUtils
from backend.src.utils.data_utils import DataUtils

fake = Faker()


@pytest.fixture
def login_payload(registered_user_credentials):
    return LoginRequest(
        username=registered_user_credentials.username,
        password=registered_user_credentials.password
    )


@pytest.fixture
def register_payload():
    valid_password = DataUtils.get_password()
    return RegisterRequest(
        username=fake.user_name(),
        password=valid_password,
        password_repeat=valid_password,
        email=f"{fake.word()}{fake.email()}"
    )


@pytest.fixture
def registered_user_credentials(auth_anonym_session, register_payload):
    auth_helper = AuthHelper(auth_anonym_session)

    auth_helper.post_register(
        register_payload.model_dump()
    )

    return LoginRequest(
        username=register_payload.username,
        password=register_payload.password
    )


@pytest.fixture
def auth_anonym_service(auth_anonym_session):
    return AuthService(auth_anonym_session)


@pytest.fixture
def auth_admin_session(access_token):
    return ApiUtils(
        url=AuthService.SERVICE_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
        }
    )


@pytest.fixture
def auth_anonym_helper(auth_anonym_session):
    return AuthHelper(api_utils=auth_anonym_session)


@pytest.fixture
def auth_invalid_token_session():
    return ApiUtils(
        url=AuthService.SERVICE_URL,
        headers={
            "Authorization": "Bearer invalid_token",
        }
    )
