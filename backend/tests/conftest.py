import time

import pytest
import requests
from faker import Faker

from backend.src.services.authentication.auth_service import AuthService
from backend.src.services.authentication.models.request.login_request import LoginRequest
from backend.src.services.authentication.models.request.register_request import RegisterRequest
from backend.src.services.universirty.university_service import UniversityService
from backend.src.utils.api_utils import ApiUtils
from backend.src.utils.data_utils import DataUtils

fake = Faker()


def _wait_service(endpoint: str, service_name: str):
    timeout = 180
    start_time = time.time()
    while time.time() < start_time + timeout:
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            time.sleep(1)  # try again in 1 sec
        else:
            break
    else:
        raise RuntimeError(f"{service_name} wasn't started during {timeout} seconds")


@pytest.fixture(scope="session", autouse=True)
def auth_service_readiness():
    _wait_service(
        endpoint=AuthService.SERVICE_URL + "/docs",
        service_name="AuthService",
    )


@pytest.fixture(scope="session", autouse=True)
def university_service_readiness():
    _wait_service(
        endpoint=UniversityService.SERVICE_URL + "/docs",
        service_name="UniversityService",
    )


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
