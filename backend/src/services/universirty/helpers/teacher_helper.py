import allure
import requests

from backend.src.services.general.helpers.base_helper import BaseHelper


class TeacherHelper(BaseHelper):
    ENDPOINT_PREFIX = "/teachers"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    TEACHER_ENDPOINT = f"{ENDPOINT_PREFIX}/{{teacher_id}}/"

    @allure.step("Создание преподавателя")
    def post_teacher(self, json: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.ROOT_ENDPOINT,
            json=json
        )
        return response

    @allure.step("Удаление преподавателя")
    def delete_teacher(self, teacher_id: int) -> requests.Response:
        response = self.api_utils.delete(
            endpoint=TeacherHelper.TEACHER_ENDPOINT.format(teacher_id=teacher_id)
        )
        return response
