import allure
import pytest
from faker import Faker

from backend.src.services.authentication.auth_service import AuthService
from backend.src.services.authentication.helpers.user_helper import UserHelper
from backend.src.services.authentication.models.response.user_response import UserResponse
from backend.src.services.general.models.response.success_response import SuccessResponse
from backend.src.utils.api_utils import ApiUtils

fake = Faker()


@allure.feature("Получение информации о пользователе")
@pytest.mark.positive
@pytest.mark.contract
class TestUserContractPositive:
    @allure.title("Информация успешно получена")
    def test_user_success_get_me(self, access_token):
        user_helper = UserHelper(
            api_utils=ApiUtils(
                url=AuthService.SERVICE_URL,
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            ),
        )
        response = user_helper.get_me()

        with allure.step("Получен статус код 200"):
            assert response.status_code == 200, (
                f"Wrong status code\n"
                f"Expected: {200}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Ответ соответствует контракту"):
            UserResponse.model_validate(response.json())


@allure.feature("Получение информации о пользователе")
@pytest.mark.negative
@pytest.mark.contract
class TestUserContractNegative:
    @allure.title("Информация не может быть получена без подтверждения прав пользователя")
    def test_user_get_me_invalid_token(self, auth_invalid_token_session):
        user_helper = UserHelper(auth_invalid_token_session)

        response = user_helper.get_me()

        with allure.step("Получен статус код 401"):
            assert response.status_code == 401, (
                f"Wrong status code\n"
                f"Expected: {401}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Ответ соответствует контракту"):
            SuccessResponse.model_validate(response.json())

    @allure.title("Информация про анонимного пользователя не может быть получена")
    def test_user_get_me_no_token(self, auth_anonym_session):
        user_helper = UserHelper(auth_anonym_session)

        response = user_helper.get_me()

        with allure.step("Получен статус код 401"):
            assert response.status_code == 401, (
                f"Wrong status code\n"
                f"Expected: {401}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Ответ соответствует контракту"):
            SuccessResponse.model_validate(response.json())
