from backend.src.services.authentication.helpers.auth_helper import AuthHelper
from backend.src.services.authentication.helpers.user_helper import UserHelper
from backend.src.services.authentication.models.request.login_request import LoginRequest
from backend.src.services.authentication.models.request.register_request import RegisterRequest
from backend.src.services.authentication.models.response.login_response import LoginResponse
from backend.src.services.authentication.models.response.user_response import UserResponse
from backend.src.services.general.base_service import BaseService
from backend.src.services.general.models.response.success_response import SuccessResponse
from backend.src.utils.api_utils import ApiUtils


class AuthService(BaseService):
    SERVICE_URL = "http://localhost:8000"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)
        self.auth_helper = AuthHelper(self.api_utils)
        self.user_helper = UserHelper(self.api_utils)

    def register_user(self, register_request: RegisterRequest) -> SuccessResponse:
        response = self.auth_helper.post_register(
            data=register_request.model_dump()
        )
        return SuccessResponse(**response.json())

    def login_user(self, login_request: LoginRequest) -> LoginResponse:
        response = self.auth_helper.post_login(
            data=login_request.model_dump()
        )
        return LoginResponse(**response.json())

    def get_user(self) -> UserResponse:
        response = self.user_helper.get_me()

        return UserResponse(**response.json())
