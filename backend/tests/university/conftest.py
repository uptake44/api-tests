from random import choice, randint

import pytest
from faker import Faker

from backend.src.services.general.enums import GradeCount
from backend.src.services.universirty.models.base_grade import GradeLimits
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
        grade=randint(GradeLimits.MIN, GradeLimits.MAX)
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

    return response


@pytest.fixture
def group_factory(university_admin_service):
    group_ids = []

    def _factory():
        response = university_admin_service.create_group(
            group_request=GroupRequest(
                name=fake.word()
            )
        )
        group_ids.append(response.id)
        return response

    yield _factory

    for group_id in group_ids:
        university_admin_service.delete_group(group_id)


@pytest.fixture
def student_factory(university_admin_service, group_factory):
    student_ids = []

    def _factory():
        group = group_factory()
        response = university_admin_service.create_student(
            student_request=StudentRequest(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                degree=choice([degree for degree in DegreeEnum]),
                phone=fake.numerify("+7##########"),
                group_id=group.id
            ),
        )
        student_ids.append(response.id)
        return response

    yield _factory

    for student_id in student_ids:
        university_admin_service.delete_student(student_id)


@pytest.fixture
def teacher_factory(university_admin_service):
    teacher_ids = []

    def _factory():
        response = university_admin_service.create_teacher(
            teacher_request=TeacherRequest(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                subject=choice([subject for subject in SubjectEnum])
            ),
        )
        teacher_ids.append(response.id)
        return response

    yield _factory

    for teacher_id in teacher_ids:
        university_admin_service.delete_teacher(teacher_id)


@pytest.fixture
def student_grades(
        university_admin_service,
        created_student,
        created_teacher
):
    student_grades = []
    created_grade_ids = []
    for _ in range(GradeCount.MIN, GradeCount.MAX):
        response = university_admin_service.create_grade(
            GradeRequest(
                student_id=created_student.id,
                teacher_id=created_teacher.id,
                grade=randint(GradeLimits.MIN, GradeLimits.MAX)
            )
        )
        student_grades.append(response.grade)
        created_grade_ids.append(response.id)

    yield student_grades

    for grade_id in created_grade_ids:
        university_admin_service.delete_grade(grade_id)


@pytest.fixture
def created_grades(grade_factory):
    grades = []
    for _ in range(GradeCount.MIN, GradeCount.MAX):
        response = grade_factory()
        grades.append(response.grade)
    return grades


@pytest.fixture
def grade_factory(
        university_admin_service,
        student_factory,
        teacher_factory
):
    grade_ids = []

    def _factory():
        student = student_factory()
        teacher = teacher_factory()

        response = university_admin_service.create_grade(
            grade_request=GradeRequest(
                teacher_id=teacher.id,
                student_id=student.id,
                grade=randint(GradeLimits.MIN, GradeLimits.MAX)
            )
        )
        grade_ids.append(response.id)
        return response

    yield _factory

    for grade_id in grade_ids:
        university_admin_service.delete_grade(grade_id)
