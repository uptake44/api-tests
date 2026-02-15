import allure
import requests

from backend.src.services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GRADE_ENDPOINT = f"{ENDPOINT_PREFIX}/{{grade_id}}"
    STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats"

    @allure.step("Создание оценки")
    def post_grade(self, data: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.ROOT_ENDPOINT,
            data=data
        )
        return response

    @allure.step("Получение оценок")
    def get_grades(
            self,
            student_id: int | None = None,
            teacher_id: int | None = None,
            group_id: int | None = None,
    ) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.ROOT_ENDPOINT,
            params={
                k: v for k, v in {
                    "student_id": student_id,
                    "teacher_id": teacher_id,
                    "group_id": group_id,
                }.items()
                if v is not None
            }
        )
        return response

    @allure.step("Получение статистики оценок")
    def get_grades_stats(
            self,
            student_id: int | None = None,
            teacher_id: int | None = None,
            group_id: int | None = None,
            **kwargs
    ) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.STATS_ENDPOINT,
            params={
                k: v
                for k, v in {
                    "student_id": student_id,
                    "teacher_id": teacher_id,
                    "group_id": group_id
                }.items()
                if v is not None
            }
        )
        return response

    @allure.step("Удаление оценки")
    def delete_grade(self, grade_id: int) -> requests.Response:
        response = self.api_utils.delete(
            endpoint=self.GRADE_ENDPOINT.format(grade_id=grade_id)
        )
        return response
