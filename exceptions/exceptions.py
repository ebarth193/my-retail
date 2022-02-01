from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class Message:
    message: str


@dataclass_json
@dataclass
class ModeledApiException:
    errors: List[Message]


class ApiException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        api_exception = {'errors': []}
        api_exception['errors'].append({'message': self.message})
        return api_exception
