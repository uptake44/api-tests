import allure
import pytest
from faker import Faker

fake = Faker()


@allure.feature("Студент")
@pytest.mark.positive
@pytest.mark.business
class TestStudentPositive:
    @allure.title("Студент привязан к своей группе")
    def test_student_create_successful(
            self,
            created_student,
            created_group,
            group_payload,
            university_admin_service
    ):
        with allure.step("Созданный студент привязан к своей группе"):
            assert created_student.group_id == created_group.id, (
                f"Wrong group id\n"
                f"Actual student group id: {created_student.group_id}\n"
                f"Expected group id: {created_group.id}"
            )
