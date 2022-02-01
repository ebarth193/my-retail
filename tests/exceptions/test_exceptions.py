import unittest
from exceptions.exceptions import (
    ApiException,
    ModeledApiException,
    Message
)


class ExceptionsTestCase(unittest.TestCase):

    def test_api_exception_to_dict(self):
        test_exception = ApiException('test exception', 500)
        expected = {
            'errors': [
                {
                    'message': 'test exception'
                }
            ]
        }
        result = test_exception.to_dict()
        self.assertEqual(result, expected)

    def test_modeled_api_exception_returns_list_of_errors(self):
        mock_message = 'test exception message'
        result = ModeledApiException(
            errors=[
                Message(message=mock_message)
            ]
        )
        self.assertEqual(len(result.errors), 1)
        self.assertEqual(result.errors[0].message, mock_message)
