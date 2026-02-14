import allure
import pytest
from faker import Faker

from backend.src.services.authentication.models.response.login_response import LoginResponse
from backend.src.services.general.enums import ValidationErrorType
from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.general.models.response.success_response import SuccessResponse
from backend.src.services.authentication.enums import ResponseMessage

fake = Faker()


@allure.feature("Авторизация")
@pytest.mark.positive
@pytest.mark.contract
class TestLoginContractPositive:
    @allure.title("Пользователь может войти с верными даннымии")
    def test_user_login_successful(
            self,
            auth_anonym_helper,
            login_payload
    ):
        login_response = auth_anonym_helper.post_login(
            data=login_payload.model_dump()
        )

        with allure.step("Получен статус код 200"):
            assert login_response.status_code == 200, (
                f"Wrong status code\n"
                f"Expected: {200}\n"
                f"Actual: {login_response.status_code}"
            )

        with allure.step("Ответ соответствует контракту"):
            LoginResponse.model_validate(login_response.json())


@allure.feature("Авторизация")
@pytest.mark.negative
@pytest.mark.contract
class TestLoginContractNegative:
    @allure.title("Авторизация не проходит без обязательного поля")
    @pytest.mark.parametrize(
        "exclude_field",
        [
            pytest.param("username", id="no_username"),
            pytest.param("password", id="no_password")
        ]
    )
    def test_login_payload_no_required_field(
            self,
            auth_anonym_helper,
            login_payload,
            exclude_field
    ):
        response = auth_anonym_helper.post_login(
            login_payload.model_dump(exclude=exclude_field)
        )

        with allure.step("Получен статус код 422"):
            assert response.status_code == 422, (
                f"Wrong status code\n"
                f"Expected: {422}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Ответ соответствует контракту"):
            validation_error_model = HTTPValidationError.model_validate(
                response.json()
            )
            actual_error_type = validation_error_model.detail[0].type
            with allure.step("Получена ошибка отсутствия обязательного поля"):
                assert actual_error_type == ValidationErrorType.NO_REQUIRED_FIELD, (
                    f"Wrong validation error type\n"
                    f"Expected: {ValidationErrorType.NO_REQUIRED_FIELD}\n"
                    f"Actual: {actual_error_type}\n"
                )

    @allure.title("Авторизация не проходит с неверными данными")
    @pytest.mark.parametrize(
        "modified_credentials",
        [
            pytest.param(
                {
                    "username": fake.user_name()
                },
                id="wrong_username"
            ),
            pytest.param(
                {
                    "password": fake.password()
                },
                id="wrong_password"
            )
        ]
    )
    def test_wrong_user_credentials(
            self,
            auth_anonym_helper,
            modified_credentials,
            login_payload
    ):
        with allure.step("Подготовка данных"):
            data = login_payload.model_dump()
            data.update(modified_credentials)

        response = auth_anonym_helper.post_login(
            data=data
        )

        with allure.step("Получен статус код 401"):
            assert response.status_code == 401, (
                f"Wrong status code\n"
                f"Expected: {401}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Ответ соответствует контракту"):
            login_response = SuccessResponse.model_validate(response.json())
            with allure.step("Получена ошибка о неверных данных"):
                assert login_response.detail == ResponseMessage.INVALID_LOGIN, (
                    f"Wrong response message\n"
                    f"Expected: {ResponseMessage.INVALID_LOGIN}\n"
                    f"Actual: {login_response.detail}\n"
                )
