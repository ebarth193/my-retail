import unittest
import requests
import properties
import json
from unittest.mock import patch
from external_dependencies.redsky import Redsky


class MockResponse:
    def __init__(self, text):
        self.status_code = 200
        self.text = text

    def raise_for_status(self):
        pass


class TestRedsky(unittest.TestCase):
    def setUp(self):
        self.mock_product_id = '123PRODUCTID'
        self.rs = Redsky()
        self.mock_response = '{"data": {"product": {"item": "some product data", "tcin": "123PRODUCTID"}}}'
        self.mock_product_info = json.loads(self.mock_response).get('data', {}).get('product', {}).get('item', {})

    @patch.object(properties, 'get_property')
    @patch.object(requests, 'get')
    def test_get_product_calls_get_property_for_URL(self, mock_get, mock_get_property):
        mock_rsp = MockResponse(self.mock_response)
        mock_get.return_value = mock_rsp
        mock_get_property.return_value = 'https://www.redsky.com'
        self.rs.get_product(self.mock_product_id)
        mock_get_property.assert_called_with('local', 'REDSKY_URL')
        mock_get.assert_called_with(mock_get_property.return_value + f'&tcin={self.mock_product_id}')

    @patch.object(properties, 'get_property')
    @patch.object(requests, 'get')
    def test_get_returns_product_info(self, mock_get, mock_get_property):
        mock_rsp = MockResponse(self.mock_response)
        mock_get.return_value = mock_rsp
        result = self.rs.get_product(self.mock_product_id)
        self.assertEqual(result, self.mock_product_info)
