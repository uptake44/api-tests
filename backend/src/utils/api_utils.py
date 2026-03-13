import json

import curlify
import requests
from requests import Session

from .json_utils import JsonUtils
from ..logger.logger import Logger


def log_response(func):
    def _log_response(*args, **kwargs) -> requests.Response:
        response = func(*args, **kwargs)
        Logger.info(f"Request: {curlify.to_curl(response.request)}")
        body = json.dumps(
            response.json(), indent=2
        ) if JsonUtils.is_json(response.text) else response.text
        Logger.info(f"Response status code='{response.status_code}', "
                    f"elapsed time='{response.elapsed}'\n{body}\n")
        return response

    return _log_response


class ApiUtils:
    def __init__(self, url: str, headers: dict | None = None):
        if headers is None:
            headers = {}

        self._session = Session()
        self._session.headers.update(headers)

        self._url = url

    @log_response
    def get(self, endpoint, **kwargs):
        response = self._session.get(self._url + endpoint, **kwargs)
        return response

    @log_response
    def post(self, endpoint, data=None, json=None, **kwargs):
        response = self._session.post(
            self._url + endpoint,
            data=data,
            json=json,
            **kwargs
        )
        return response

    @log_response
    def put(self, endpoint, data=None, **kwargs):
        response = self._session.put(
            self._url + endpoint,
            data=data,
            json=json,
            **kwargs
        )
        return response

    @log_response
    def delete(self, endpoint, **kwargs):
        response = self._session.delete(
            self._url + endpoint,
            **kwargs
        )
        return response
