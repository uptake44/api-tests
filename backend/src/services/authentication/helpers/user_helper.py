import allure
import requests

from backend.src.services.general.helpers.base_helper import BaseHelper


class UserHelper(BaseHelper):
    ENDPOINT_PREFIX = "/users"

    ME_ENDPOINT = f"{ENDPOINT_PREFIX}/me"

    @allure.step("Получение информации о пользователе")
    def get_me(self) -> requests.Response:
        response = self.api_utils.get(
            endpoint=self.ME_ENDPOINT,
        )
        return response
