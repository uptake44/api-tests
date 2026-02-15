import allure
import pytest
from faker import Faker

from backend.src.services.authentication.models.request.register_request import RegisterRequest
from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.authentication.enums import ResponseMessage
from backend.src.utils.data_utils import DataUtils

fake = Faker()


@allure.feature("Проверка пароля")
@pytest.mark.negative
@pytest.mark.business
class TestPasswordValidationNegative:
    @allure.title("Пароль соответствует требованиям")
    @pytest.mark.parametrize(
        "password",
        [
            pytest.param(
                DataUtils.get_password(length=6),
                id="short_password"
            ),
            pytest.param(
                DataUtils.get_password(length=101),
                id="long_password"
            ),
            pytest.param(
                DataUtils.get_password(special_chars=False),
                id="no_special_chars"
            ),
            pytest.param(
                DataUtils.get_password(digits=False),
                id="no_digits"
            ),
            pytest.param(
                "",
                id="empty_password"
            )
        ]
    )
    def test_register_password_validation(
            self,
            auth_anonym_helper,
            register_payload,
            password
    ):
        with allure.step("Подготовка данных"):
            payload = register_payload.model_dump()
            payload.update(
                {"password": password}
            )

        response = auth_anonym_helper.post_register(
            data=payload
        )

        with allure.step("Получен статус код 422"):
            assert response.status_code == 422, (
                f"Wrong status code\n"
                f"Expected: {422}\n"
                f"Actual: {response.status_code}"
            )

        with allure.step("Получена ошибка о неподходящем пароле"):
            HTTPValidationError.model_validate(response.json())


@allure.feature("Конфликт данных при регистрации")
@pytest.mark.negative
@pytest.mark.business
class TestRegistrationConflictNegative:
    @allure.title("Регистрация отклоняется при уже существующем username")
    def test_username_must_be_unique(self, auth_anonym_service):
        with allure.step("Подготовка данных"):
            password = DataUtils.get_password()
            user = RegisterRequest(
                username=fake.user_name(),
                password=password,
                password_repeat=password,
                email=fake.email(),
            )
            auth_anonym_service.register_user(user)

        response = auth_anonym_service.register_user(user)

        with allure.step("Получена ошибка 'username уже занят'"):
            assert response.detail == ResponseMessage.USERNAME_TAKEN, (
                f"Wrong response message\n"
                f"Expected: {ResponseMessage.USERNAME_TAKEN}\n"
                f"Actual: {response.detail}"
            )

    @allure.title("Регистрация отклоняется при уже существующем email")
    def test_email_must_be_unique(self, auth_anonym_service):
        with allure.step("Подготовка данных"):
            password = DataUtils.get_password()
            email = fake.email()
            first_user = RegisterRequest(
                username=fake.user_name(),
                password=password,
                password_repeat=password,
                email=email,
            )
            second_user = first_user.model_copy(
                update={"username": fake.user_name()}
            )
            auth_anonym_service.register_user(first_user)

        response = auth_anonym_service.register_user(second_user)

        with allure.step("Получена ошибка 'email уже занят'"):
            assert response.detail == ResponseMessage.EMAIL_TAKEN, (
                f"Wrong response message\n"
                f"Expected: {ResponseMessage.EMAIL_TAKEN}\n"
                f"Actual: {response.detail}"
            )
