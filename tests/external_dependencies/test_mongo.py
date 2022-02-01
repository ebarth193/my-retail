import unittest
import properties
import json
from unittest.mock import patch, call
from external_dependencies.mongo import Mongo
from exceptions.exceptions import ApiException


class MockResponse:
    def __init__(self, text):
        self.status_code = 200
        self.text = text

    def raise_for_status(self):
        pass


class TestMongo(unittest.TestCase):
    def setUp(self):
        self.mock_product_id = '123PRODUCTID'
        self.mgo = Mongo()
        self.mock_response = '{"data": {"product": {"item": "some product data", "tcin": "123PRODUCTID"}}}'
        self.mock_product_info = json.loads(self.mock_response).get('data', {}).get('product', {}).get('item', {})

    @patch.object(Mongo, 'create_mongo_client')
    @patch.object(properties, 'get_property')
    def test_get_db_client_calls_get_property(self, mock_get_property, mock_create_mongo_client):
        mock_get_property.side_effect = ['TEST_USER', 'TEST_PASS', 'TEST_URL', 'TEST_DB_NAME']
        self.mgo.get_db_client()
        mock_get_property.assert_has_calls([
            call('local', 'MONGO_DB_USER'),
            call('local', 'MONGO_DB_PASS'),
            call('local', 'MONGO_URL'),
            call('local', 'MONGO_DB_NAME')
        ])
        mock_conn_str = 'mongodb+srv://TEST_USER:TEST_PASSTEST_URL'
        mock_create_mongo_client.assert_called_with(mock_conn_str)

    @patch.object(Mongo, 'create_mongo_client')
    @patch.object(properties, 'get_property')
    def test_get_db_client_raises_ApiException(self, mock_get_property, mock_create_mongo_client):
        mock_get_property.side_effect = ['TEST_USER', 'TEST_PASS', 'TEST_URL', 'TEST_DB_NAME']
        mock_create_mongo_client.side_effect = ApiException(message='TEST EXCEPTION')
        with self.assertRaises(ApiException):
            self.mgo.get_db_client()
