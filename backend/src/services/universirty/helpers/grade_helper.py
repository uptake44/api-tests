import requests

from backend.src.services.general.helpers.base_helper import BaseHelper


class GradeHelper(BaseHelper):
    ENDPOINT_PREFIX = "/grades"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GRADE_ENDPOINT = f"{ENDPOINT_PREFIX}/{{grade_id}}"
    STATS_ENDPOINT = f"{ENDPOINT_PREFIX}/stats"

    def post_grades(self, data: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.ROOT_ENDPOINT,
            data=data
        )
        return response

    def get_grades(self, params: dict | None = None) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.ROOT_ENDPOINT,
            params=params
        )
        return response

    def get_grades_stats(self, params: dict | None = None) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.STATS_ENDPOINT,
            params=params
        )
        return response

    def delete_grade(self, grade_id: int) -> requests.Response:
        response = self.api_utils.delete(
            endpoint=self.GRADE_ENDPOINT.format(grade_id=grade_id)
        )
        return response
