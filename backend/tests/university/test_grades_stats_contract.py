import pytest
from faker import Faker

from backend.src.services.general.models.response.http_validation_error import HTTPValidationError
from backend.src.services.general.models.response.success_response import SuccessResponse
from backend.src.services.universirty.helpers.grade_helper import GradeHelper
from backend.src.services.universirty.models.response.grade_stats_response import GradeStatsResponse

fake = Faker()


@pytest.mark.contract
@pytest.mark.positive
class TestGradesStatsPositiveContract:
    def test_get_grades_stats_success(
            self,
            university_admin_session
    ):
        grade_helper = GradeHelper(university_admin_session)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 200, (
            "Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {200}\n"
        )
        GradeStatsResponse.model_validate(response.json())


@pytest.mark.contract
@pytest.mark.negative
class TestGradesStatsNegativeContract:
    def test_get_grades_stats_no_token(
            self,
            university_anonym_session
    ):
        grade_helper = GradeHelper(university_anonym_session)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 401, (
            "Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {401}\n"
        )
        SuccessResponse.model_validate(response.json())

    def test_get_grades_stats_invalid_token(
            self,
            university_invalid_token_session
    ):
        grade_helper = GradeHelper(university_invalid_token_session)

        response = grade_helper.get_grades_stats()

        assert response.status_code == 401, (
            "Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {401}\n")
        SuccessResponse.model_validate(response.json())

    def test_get_grades_stats_extra_param(
            self,
            university_admin_session
    ):
        grade_helper = GradeHelper(university_admin_session)

        response = grade_helper.get_grades_stats(
            extra_param=fake.word()
        )

        assert response.status_code == 422, (
            "Wrong status code\n"
            f"Actual: {response.status_code}\n"
            f"Expected: {422}\n")
        HTTPValidationError.model_validate(response.json())
