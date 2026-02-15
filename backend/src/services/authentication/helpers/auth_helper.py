import allure
import requests

from ...general.helpers.base_helper import BaseHelper


class AuthHelper(BaseHelper):
    ENDPOINT_PREFIX = "/auth"

    REGISTER_ENDPOINT = f"{ENDPOINT_PREFIX}/register"
    LOGIN_ENDPOINT = f"{ENDPOINT_PREFIX}/login"

    @allure.step("Регистрация пользователя")
    def post_register(self, data: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.REGISTER_ENDPOINT,
            data=data,
        )
        return response

    @allure.step("Авторизация пользователя")
    def post_login(self, data: dict) -> requests.Response:
        response = self.api_utils.post(
            endpoint=self.LOGIN_ENDPOINT,
            data=data,
        )
        return response
