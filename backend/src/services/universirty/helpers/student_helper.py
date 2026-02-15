import allure
import requests

from backend.src.services.general.helpers.base_helper import BaseHelper


class StudentHelper(BaseHelper):
    ENDPOINT_PREFIX = "/students"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    STUDENT_ENDPOINT = f"{ENDPOINT_PREFIX}/{{student_id}}/"

    @allure.step("Получение студентов")
    def get_students(self) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.ROOT_ENDPOINT,
        )
        return response

    @allure.step("Создание студента")
    def post_student(self, json: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.ROOT_ENDPOINT,
            json=json,
        )
        return response

    @allure.step("Удаление студента")
    def delete_student(self, student_id: int) -> requests.Response:
        response = self.api_utils.delete(
            endpoint=self.STUDENT_ENDPOINT.format(student_id=student_id),
        )
        return response

    @allure.step("Получение студента")
    def get_student(self, student_id: str) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.STUDENT_ENDPOINT.format(student_id=student_id),
        )
        return response

    @allure.step("Изменение студента")
    def put_student(self, student_id: str, json: dict) -> requests.Response:
        response = self.api_utils.put(
            endpoint=self.STUDENT_ENDPOINT.format(student_id=student_id),
            json=json
        )
        return response
