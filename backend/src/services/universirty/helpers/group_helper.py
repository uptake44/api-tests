import allure
import requests

from backend.src.services.general.helpers.base_helper import BaseHelper


class GroupHelper(BaseHelper):
    ENDPOINT_PREFIX = "/groups"

    ROOT_ENDPOINT = f"{ENDPOINT_PREFIX}/"
    GROUP_ENDPOINT = f"{ENDPOINT_PREFIX}/{{group_id}}"

    @allure.step("Получение групп")
    def get_groups(self) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.ROOT_ENDPOINT,
        )
        return response

    @allure.step("Создание группы")
    def post_group(self, json: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.ROOT_ENDPOINT,
            json=json
        )
        return response

    @allure.step("Удаление группы")
    def delete_group(self, group_id: int) -> requests.Response:
        response = self.api_utils.delete(
            endpoint=self.GROUP_ENDPOINT.format(group_id=group_id)
        )
        return response
