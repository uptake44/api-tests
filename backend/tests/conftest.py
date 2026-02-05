import pytest
from faker import Faker

from backend.src.services.authentication.auth_service import AuthService
from backend.src.services.authentication.models.request.login_request import LoginRequest
from backend.src.services.authentication.models.request.register_request import RegisterRequest
from backend.src.utils.api_utils import ApiUtils
from backend.src.utils.data_utils import DataUtils

fake = Faker()


@pytest.fixture
def auth_anonym_session():
    return ApiUtils(
        url=AuthService.SERVICE_URL
    )


@pytest.fixture
def access_token(auth_anonym_session):
    auth_service = AuthService(auth_anonym_session)
    username = fake.user_name()
    password = DataUtils.get_password()
    email = fake.email()

    auth_service.register_user(
        register_request=RegisterRequest(
            username=username,
            password=password,
            password_repeat=password,
            email=email,
        )
    )

    login_response = auth_service.login_user(
        login_request=LoginRequest(
            username=username,
            password=password,
        )
    )

    return login_response.access_token


