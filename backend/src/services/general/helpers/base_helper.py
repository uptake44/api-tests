from backend.src.utils.api_utils import ApiUtils


class BaseHelper:
    ENDPOINT_PREFIX = None  # Переопределяется в наследнике

    def __init__(self, api_utils: ApiUtils):
        self.api_utils = api_utils
