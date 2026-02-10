import pytest
from faker import Faker

from backend.src.services.authentication.models.response.login_response import LoginResponse
from backend.src.services.general.enums import ValidationErrorType, ResponseMessage
from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.general.models.response.success_response import SuccessResponse

fake = Faker()


@pytest.mark.positive
@pytest.mark.contract
class TestLoginContractPositive:
    def test_user_login_successful(
            self,
            auth_anonym_helper,
            login_payload
    ):
        login_response = auth_anonym_helper.post_login(
            data=login_payload.model_dump()
        )

        assert login_response.status_code == 200, (
            f"Wrong status code\n"
            f"Expected: {200}\n"
            f"Actual: {login_response.status_code}"
        )

        LoginResponse.model_validate(login_response.json())


@pytest.mark.negative
class TestLoginContractNegative:
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

        assert response.status_code == 422, (
            f"Wrong status code\n"
            f"Expected: {422}\n"
            f"Actual: {response.status_code}"
        )

        validation_error_model = HTTPValidationError.model_validate(
            response.json()
        )

        actual_error_type = validation_error_model.detail[0].type
        assert actual_error_type == ValidationErrorType.NO_REQUIRED_FIELD, (
            f"Wrong validation error type\n"
            f"Expected: {ValidationErrorType.NO_REQUIRED_FIELD}\n"
            f"Actual: {actual_error_type}\n"
        )

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
        data = login_payload.model_dump()
        data.update(modified_credentials)

        response = auth_anonym_helper.post_login(
            data=data
        )

        assert response.status_code == 401, (
            f"Wrong status code\n"
            f"Expected: {401}\n"
            f"Actual: {response.status_code}"
        )

        login_response = SuccessResponse.model_validate(response.json())
        assert login_response.detail == ResponseMessage.INVALID_LOGIN, (
            f"Wrong response message\n"
            f"Expected: {ResponseMessage.INVALID_LOGIN}\n"
            f"Actual: {login_response.detail}\n"
        )
