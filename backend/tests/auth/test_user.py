import pytest

from backend.src.services.authentication.auth_service import AuthService
from backend.src.services.authentication.models.request.login_request import LoginRequest
from backend.src.utils.api_utils import ApiUtils

@pytest.mark.positive
@pytest.mark.business
class TestUserPositive:
    def test_get_authorized_user_info(
            self,
            registered_user_credentials,
            auth_anonym_session
    ):
        auth_service_anonym = AuthService(auth_anonym_session)

        username = registered_user_credentials.username
        password = registered_user_credentials.password
        login_response = auth_service_anonym.login_user(
            login_request=LoginRequest(
                username=username,
                password=password
            )
        )

        user_service = AuthService(
            ApiUtils(
                url=AuthService.SERVICE_URL,
                headers={
                    "Authorization": f"Bearer {login_response.access_token}"
                }
            )
        )
        user_response = user_service.get_user()

        assert user_response.username == username, (
            f"Wrong username\n",
            f"Expected: {username}\n"
            f"Actual: {user_response.username}"
        )
