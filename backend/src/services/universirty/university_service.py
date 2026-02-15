from backend.src.services.general.base_service import BaseService
from backend.src.services.general.models.response.success_response import SuccessResponse
from backend.src.services.universirty.helpers.grade_helper import GradeHelper
from backend.src.services.universirty.helpers.group_helper import GroupHelper
from backend.src.services.universirty.helpers.student_helper import StudentHelper
from backend.src.services.universirty.helpers.teacher_helper import TeacherHelper
from backend.src.services.universirty.models.request.grade_request import GradeRequest
from backend.src.services.universirty.models.request.group_request import GroupRequest
from backend.src.services.universirty.models.request.student_request import StudentRequest
from backend.src.services.universirty.models.request.teacher_request import TeacherRequest
from backend.src.services.universirty.models.response.grade_response import GradeResponse, AllGradesResponse
from backend.src.services.universirty.models.response.grade_stats_response import GradeStatsResponse
from backend.src.services.universirty.models.response.group_response import GroupResponse
from backend.src.services.universirty.models.response.student_response import (StudentResponse,
                                                                               AllStudentsResponse)
from backend.src.services.universirty.models.response.teacher_response import TeacherResponse
from backend.src.utils.api_utils import ApiUtils


class UniversityService(BaseService):
    SERVICE_URL = "http://localhost:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)
        self.student_helper = StudentHelper(self.api_utils)
        self.group_helper = GroupHelper(self.api_utils)
        self.teacher_helper = TeacherHelper(self.api_utils)
        self.grade_helper = GradeHelper(self.api_utils)

    def get_all_students(self) -> AllStudentsResponse:
        response = self.student_helper.get_students()
        return AllStudentsResponse(students=response.json())

    def create_student(
            self,
            student_request: StudentRequest
    ) -> StudentResponse:
        response = self.student_helper.post_student(
            json=student_request.model_dump()
        )
        return StudentResponse(**response.json())

    def delete_student(self, student_id: int) -> SuccessResponse:
        response = self.student_helper.delete_student(
            student_id
        )
        return SuccessResponse(**response.json())

    def create_group(self, group_request: GroupRequest) -> GroupResponse:
        response = self.group_helper.post_group(
            json=group_request.model_dump()
        )
        return GroupResponse(**response.json())

    def delete_group(self, group_id: int) -> SuccessResponse:
        response = self.group_helper.delete_group(group_id)
        return SuccessResponse(**response.json())

    def create_teacher(
            self,
            teacher_request: TeacherRequest
    ) -> TeacherResponse:
        response = self.teacher_helper.post_teacher(
            json=teacher_request.model_dump()
        )
        return TeacherResponse(**response.json())

    def delete_teacher(self, teacher_id: int) -> SuccessResponse:
        response = self.teacher_helper.delete_teacher(teacher_id)
        return SuccessResponse(**response.json())

    def create_grade(self, grade_request: GradeRequest) -> GradeResponse:
        response = self.grade_helper.post_grade(
            data=grade_request.model_dump()
        )
        return GradeResponse(**response.json())

    def delete_grade(self, grade_id: int) -> SuccessResponse:
        response = self.grade_helper.delete_grade(grade_id)
        return SuccessResponse(**response.json())

    def get_grades(
            self,
            student_id: int | None = None,
            teacher_id: int | None = None,
            group_id: int | None = None,
    ) -> AllGradesResponse:
        response = self.grade_helper.get_grades(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )
        return AllGradesResponse(grades=response.json())


    def get_grades_stats(
            self,
            student_id: int | None = None,
            teacher_id: int | None = None,
            group_id: int | None = None
    ) -> GradeStatsResponse:
        response = self.grade_helper.get_grades_stats(
            student_id=student_id,
            teacher_id=teacher_id,
            group_id=group_id
        )
        return GradeStatsResponse(**response.json())
