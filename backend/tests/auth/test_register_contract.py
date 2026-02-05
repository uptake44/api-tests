import pytest
from faker import Faker

from backend.src.services.general.enums import ValidationErrorType
from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.general.models.response.success_response import SuccessResponse

fake = Faker()


@pytest.mark.positive
@pytest.mark.contract
class TestRegistrationContractPositive:
    def test_register_successful(self, auth_anonym_helper, register_payload):
        response = auth_anonym_helper.post_register(
            data=register_payload.model_dump()
        )

        assert response.status_code == 201, (
            f"Wrong status code\n"
            f"Expected: {201}\n"
            f"Actual: {response.status_code}"
        )
        SuccessResponse.model_validate(response.json())


@pytest.mark.negative
@pytest.mark.contract
class TestRegistrationContractNegative:
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

        assert response.status_code == 422, (
            f"Wrong status code\n"
            f"Expected: {422}\n"
            f"Actual: {response.status_code}"
        )
        validation_error = HTTPValidationError.model_validate(response.json())
        assert any(
            error.type == ValidationErrorType.NO_REQUIRED_FIELD
            for error in validation_error.detail
        )

    def test_register_extra_field(
            self,
            register_payload,
            auth_anonym_helper
    ):
        data = register_payload.model_dump()
        data.update(
            {
                "bio": fake.sentence(),
            }
        )
        response = auth_anonym_helper.post_register(
            data=data
        )

        assert response.status_code == 422, (
            f"Wrong status code\n"
            f"Expected: {422}\n"
            f"Actual: {response.status_code}"
        )
        HTTPValidationError.model_validate(response.json())
