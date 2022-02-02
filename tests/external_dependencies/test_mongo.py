import unittest
import properties
import json
from unittest.mock import patch, call
from external_dependencies.mongo import Mongo
from exceptions.exceptions import ApiException
from bson.objectid import ObjectId
from dataclasses import dataclass


class MockResponse:
    def __init__(self, text):
        self.status_code = 200
        self.text = text

    def raise_for_status(self):
        pass


@dataclass
class MockUpdateResult:
    modified_count: int


class TestMongo(unittest.TestCase):
    def setUp(self):
        self.mock_product_id = '123PRODUCTID'
        self.mgo = Mongo()
        self.mock_response = '{"data": {"product": {"item": "some product data", "tcin": "123PRODUCTID"}}}'
        self.mock_product_info = json.loads(self.mock_response).get('data', {}).get('product', {}).get('item', {})
        self.mock_price_info = {"value": "10.99", "currency_code": "USD"}

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

    @patch.object(Mongo, 'find_one')
    @patch.object(properties, 'get_property')
    def test_get_product_price_calls_get_property(self, mock_get_property, mock_find_one):
        mock_get_property.return_value = 'TABLE_NAME'
        self.mgo.get_product_price(self.mock_product_id)
        mock_product_info_dict = {'product_id': self.mock_product_id}
        mock_find_one.assert_called_with(mock_get_property.return_value, mock_product_info_dict)
        mock_get_property.assert_called_with('local', 'MONGO_DB_PRICE_TABLE')

    @patch.object(Mongo, 'find_one')
    @patch.object(properties, 'get_property')
    def test_get_product_price_calls_find_one(self, mock_get_property, mock_find_one):
        mock_get_property.return_value = 'TABLE_NAME'
        self.mgo.get_product_price(self.mock_product_id)
        mock_product_info_dict = {'product_id': self.mock_product_id}
        mock_find_one.assert_called_with(mock_get_property.return_value, mock_product_info_dict)

    @patch.object(Mongo, 'find_one')
    @patch.object(properties, 'get_property')
    def test_get_product_price_returns_none_when_no_result(self, mock_get_property, mock_find_one):
        mock_get_property.return_value = 'TABLE_NAME'
        mock_find_one.return_value = None
        result = self.mgo.get_product_price(self.mock_product_id)
        self.assertEqual(result, None)

    @patch.object(Mongo, 'find_one')
    @patch.object(properties, 'get_property')
    def test_get_product_price_returns_result(self, mock_get_property, mock_find_one):
        mock_get_property.return_value = 'TABLE_NAME'
        mock_find_one.return_value = {'_id': ObjectId('61f2011a9552ecb5d6b65b8f'), 'product_id': '123PRODUCTID',
                                      'value': 13.49, 'currency_code': 'USD'}
        expected = {'_id': '61f2011a9552ecb5d6b65b8f', 'product_id': '123PRODUCTID',
                    'value': 13.49, 'currency_code': 'USD'}
        result = self.mgo.get_product_price(self.mock_product_id)
        self.assertEqual(result, expected)

    @patch.object(Mongo, 'find_one')
    @patch.object(properties, 'get_property')
    def test_get_product_price_raises_ApiException(self, mock_get_property, mock_find_one):
        mock_get_property.return_value = 'TABLE_NAME'
        mock_find_one.side_effect = ApiException(message='TEST EXCEPTION')
        with self.assertRaises(ApiException):
            self.mgo.get_product_price(self.mock_product_id)

    @patch.object(Mongo, 'update_one')
    @patch.object(properties, 'get_property')
    def test_update_product_price_returns_1_if_result(self, mock_get_property, mock_update_one):
        mock_update_one.return_value = MockUpdateResult(modified_count=1)
        result = self.mgo.update_product_price(self.mock_product_id, self.mock_price_info)
        self.assertEqual(result, 1)

    @patch.object(Mongo, 'update_one')
    @patch.object(properties, 'get_property')
    def test_update_product_price_returns_None_if_no_result(self, mock_get_property, mock_update_one):
        mock_update_one.return_value = None
        result = self.mgo.update_product_price(self.mock_product_id, self.mock_price_info)
        self.assertEqual(result, None)

    @patch.object(Mongo, 'update_one')
    @patch.object(properties, 'get_property')
    def test_get_update_product_price_raises_ApiException(self, mock_get_property, mock_update_one):
        mock_update_one.side_effect = ApiException(message='TEST EXCEPTION')
        with self.assertRaises(ApiException):
            self.mgo.update_product_price(self.mock_product_id, self.mock_price_info)
