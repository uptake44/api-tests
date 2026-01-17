from random import choice

from faker import Faker

from services.university.models.base_student import DegreeEnum
from services.university.models.group_request import GroupRequest
from services.university.models.student_request import StudentRequest
from services.university.university_service import UniversityService

faker = Faker()


class TestStudent:
    def test_student_create(self, university_api_utils_admin):
        university_service = UniversityService(
            api_utils=university_api_utils_admin,
        )
        group = GroupRequest(name=faker.name())
        group_response = university_service.create_group(
            group_request=group
        )

        student = StudentRequest(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            degree=choice([option for option in DegreeEnum]),
            phone=faker.numerify("+7##########"),
            group_id=group_response.id
        )

        student_response = university_service.create_student(
            student_request=student
        )

        assert student_response.group_id == group_response.id, (
            f"Wrong group id. Actual: {student_response.group_id},\n"
            f"Expected: {group_response.id}"
        )
