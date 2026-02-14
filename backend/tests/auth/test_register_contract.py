import allure
import pytest
from faker import Faker

from backend.src.services.general.enums import ValidationErrorType
from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.general.models.response.success_response import SuccessResponse

fake = Faker()


@allure.feature("Регистрация")
@pytest.mark.positive
@pytest.mark.contract
class TestRegistrationContractPositive:
    @allure.title("Пользователь успешно зарегистрирован")
    def test_register_successful(self, auth_anonym_helper, register_payload):
        response = auth_anonym_helper.post_register(
            data=register_payload.model_dump()
        )

        with allure.step("Получен статус код 201"):
            assert response.status_code == 201, (
                f"Wrong status code\n"
                f"Expected: {201}\n"
                f"Actual: {response.status_code}"
            )
        with allure.step("Ответ соответствует контракту"):
            SuccessResponse.model_validate(response.json())


@allure.feature("Регистрация")
@pytest.mark.negative
@pytest.mark.contract
class TestRegistrationContractNegative:
    @allure.title("Пользователь не может зарегистрироваться без обязательного поля")
    @pytest.mark.parametrize(
        "exclude_field",
        [
            pytest.param("username", id="no_username"),
            pytest.param("password", id="no_password"),
            pytest.param("password_repeat", id="no_password_repeat"),
            pytest.param("email", id="no_email")
        ]
    )
    def test_register_no_required_field(
            self,
            exclude_field,
            register_payload,
            auth_anonym_helper
    ):
        response = auth_anonym_helper.post_register(
            data=register_payload.model_dump(exclude=exclude_field)
        )

        with allure.step("Получен статус код 422"):
            assert response.status_code == 422, (
                f"Wrong status code\n"
                f"Expected: {422}\n"
                f"Actual: {response.status_code}"
            )
        with allure.step("Ответ соответствует контракту"):
            validation_error_model = HTTPValidationError.model_validate(response.json())
            actual_error_type = validation_error_model.detail[0].type
            with allure.step("Получена ошибка отсутствия поля"):
                assert actual_error_type == ValidationErrorType.NO_REQUIRED_FIELD, (
                    f"Wrong validation error type\n"
                    f"Expected: {ValidationErrorType.NO_REQUIRED_FIELD}\n"
                    f"Actual: {actual_error_type}\n"
                )

    @allure.title("Пользователь не может зарегистрироваться с дополнительно переданным полем")
    def test_register_extra_field(
            self,
            register_payload,
            auth_anonym_helper
    ):
        with allure.step("Подготовка данных"):
            data = register_payload.model_dump()
            data.update(
                {
                    "bio": fake.sentence(),
                }
            )
        response = auth_anonym_helper.post_register(
            data=data
        )

        with allure.step("Получен статус код 422"):
            assert response.status_code == 422, (
                f"Wrong status code\n"
                f"Expected: {422}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Получена ошибка о неправильном запросе"):
            HTTPValidationError.model_validate(response.json())
