from random import choice, randint

import pytest
from faker import Faker

from backend.src.services.universirty.models.base_student import DegreeEnum
from backend.src.services.universirty.models.base_teacher import SubjectEnum
from backend.src.services.universirty.models.request.grade_request import GradeRequest
from backend.src.services.universirty.models.request.group_request import GroupRequest
from backend.src.services.universirty.models.request.student_request import StudentRequest
from backend.src.services.universirty.models.request.teacher_request import TeacherRequest
from backend.src.services.universirty.university_service import UniversityService
from backend.src.utils.api_utils import ApiUtils

fake = Faker()


@pytest.fixture
def session(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def university_admin_service(university_admin_session):
    return UniversityService(university_admin_session)


@pytest.fixture
def university_anonym_session():
    return ApiUtils(
        url=UniversityService.SERVICE_URL
    )


@pytest.fixture
def university_invalid_token_session():
    return ApiUtils(
        url=UniversityService.SERVICE_URL,
        headers={
            "Authorization": f"Bearer invalid_token"
        }
    )


@pytest.fixture
def university_admin_session(access_token):
    return ApiUtils(
        url=UniversityService.SERVICE_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )


@pytest.fixture
def teacher_payload():
    return TeacherRequest(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        subject=choice([subject for subject in SubjectEnum])
    )


@pytest.fixture
def group_payload():
    return GroupRequest(
        name=fake.word()
    )


@pytest.fixture
def student_payload(created_group):
    return StudentRequest(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        degree=choice([degree for degree in DegreeEnum]),
        phone=fake.numerify("+7##########"),
        group_id=created_group.id
    )


@pytest.fixture
def grade_payload(created_teacher, created_student, created_group):
    return GradeRequest(
        teacher_id=created_teacher.id,
        student_id=created_student.id,
        grade=randint(0, 5)
    )


@pytest.fixture
def created_student(university_admin_service, student_payload):
    response = university_admin_service.create_student(
        student_request=student_payload
    )
    yield response

    university_admin_service.delete_student(response.id)


@pytest.fixture
def created_teacher(university_admin_service, teacher_payload):
    response = university_admin_service.create_teacher(
        teacher_request=teacher_payload
    )

    yield response

    university_admin_service.delete_teacher(response.id)


@pytest.fixture
def created_group(university_admin_service, group_payload):
    response = university_admin_service.create_group(
        group_request=group_payload
    )
    yield response

    university_admin_service.delete_group(response.id)
