import pytest
from faker import Faker

from backend.src.services.general.enums import ValidationErrorType
from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.general.models.response.success_response import SuccessResponse
from backend.src.services.universirty.helpers.student_helper import StudentHelper
from backend.src.services.universirty.models.response.student_response import StudentResponse

fake = Faker()


@pytest.mark.positive
@pytest.mark.contract
class TestStudentContractPositive:
    def test_create_student_success(
            self,
            university_admin_session,
            student_payload
    ):
        student_helper = StudentHelper(university_admin_session)

        response = student_helper.post_student(
            json=student_payload.model_dump()
        )

        assert response.status_code == 201, (
            f"Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {201}\n"
        )
        StudentResponse.model_validate(response.json())

    def test_get_students(self, university_admin_session, student_payload):
        student_helper = StudentHelper(university_admin_session)

        student_helper.post_student(
            json=student_payload.model_dump()
        )

        response = student_helper.get_students()

        assert response.status_code == 200, (
            f"Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {200}\n"
        )
        [StudentResponse.model_validate(item) for item in response.json()]


@pytest.mark.negative
@pytest.mark.contract
class TestStudentContractNegative:
    def test_create_student_invalid_token(self, university_invalid_token_session, student_payload):
        student_helper = StudentHelper(university_invalid_token_session)

        response = student_helper.post_student(
            json=student_payload.model_dump()
        )

        assert response.status_code == 401, (
            "Wrong status code\n"
            f"Actual: {response.status_code}"
            f"Expected: {401}\n"
        )
        SuccessResponse.model_validate(response.json())

    def test_create_student_no_token(self, university_anonym_session, student_payload):
        student_helper = StudentHelper(university_anonym_session)

        response = student_helper.post_student(
            json=student_payload.model_dump()
        )

        assert response.status_code == 401, (
            "Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {401}\n"
        )
        SuccessResponse.model_validate(response.json())

    def test_get_students_invalid_token(self, university_invalid_token_session):
        student_helper = StudentHelper(university_invalid_token_session)

        response = student_helper.get_students()

        assert response.status_code == 401, (
            f"Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {401}\n"
        )
        SuccessResponse.model_validate(response.json())

    def test_get_students_no_token(self, university_anonym_session):
        student_helper = StudentHelper(university_anonym_session)

        response = student_helper.get_students()

        assert response.status_code == 401, (
            f"Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {401}\n"
        )
        SuccessResponse.model_validate(response.json())

    @pytest.mark.parametrize(
        "exclude_field",
        [
            pytest.param("first_name", id="no_first_name"),
            pytest.param("last_name", id="no_last_name"),
            pytest.param("email", id="no_email"),
            pytest.param("degree", id="no_degree"),
            pytest.param("phone", id="no_phone"),
            pytest.param("group_id", id="no_group_id"),
        ]
    )
    def test_create_student_no_required_field(
            self,
            university_admin_session,
            student_payload,
            exclude_field
    ):
        student_helper = StudentHelper(university_admin_session)
        response = student_helper.post_student(
            json=student_payload.model_dump(exclude=exclude_field)
        )

        assert response.status_code == 422, (
            f"Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {422}\n"
        )
        validation_error = HTTPValidationError.model_validate(response.json())

        actual_validation_error = validation_error.detail[0].type
        assert actual_validation_error == ValidationErrorType.NO_REQUIRED_FIELD, (
            f"Wrong validation error\n"
            f"Actual: {validation_error}\n"
            f"Expected: {ValidationErrorType.NO_REQUIRED_FIELD}\n"
        )
