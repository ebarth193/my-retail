import urllib
import logging
import properties
from urllib import parse
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)
from exceptions.exceptions import ApiException


class Mongo:
    def __init__(self):
        self.client = self.get_db_client()

    @staticmethod
    def create_mongo_client(conn_str: str):
        return MongoClient(conn_str, serverSelectionTimeoutMS=3000)

    def get_db_client(self):
        logging.info('Attempting to create MongoClient')
        username = urllib.parse.quote_plus(properties.get_property('local', 'MONGO_DB_USER'))
        password = urllib.parse.quote_plus(properties.get_property('local', 'MONGO_DB_PASS'))
        cluster_url = properties.get_property('local', 'MONGO_URL')
        conn_str = f"mongodb+srv://{username}:{password}{cluster_url}"
        try:
            client = self.create_mongo_client(conn_str)
            database = client[properties.get_property('local', 'MONGO_DB_NAME')]
            return database
        except ConnectionFailure as e:
            logging.error('ConnectionFailure: Unable to create MongoDB client!', exc_info=True)
            raise ApiException("Internal Server Error!", status_code=500) from e
        except PyMongoError as e:
            logging.error('PyMongoError: Unable to create MongoDB client!', exc_info=True)
            raise ApiException("Internal Server Error!", status_code=500) from e

    def find_one(self, table: str, to_find: dict):
        table = self.client[table]
        return table.find_one(to_find)

    def get_product_price(self, product_id: str):
        try:
            logging.info(f"Attempting to retrieve product price for {product_id}")
            product_info = {'product_id': product_id}
            result = self.find_one(properties.get_property('local', 'MONGO_DB_PRICE_TABLE'), product_info)
            if result:
                logging.info(f"Successfully retrieved product price for {product_id}")
                # Convert the ObjectId to a string
                # https://docs.mongodb.com/manual/reference/bson-types/#std-label-objectid
                result['_id'] = str(result.get('_id'))
                return result
            logging.info(f"No price found for product id {product_id}")
            return None
        except OperationFailure as e:
            logging.error(f'OperationFailure: Unable to retrieve product price for product id {product_id}',
                          exc_info=True)
            raise ApiException(f'Internal Server Error: Unable to retrieve product price for product id {product_id}',
                               status_code=500)
        except PyMongoError as e:
            logging.error(f'PyMongoError: Unable to retrieve product price for product id {product_id}', exc_info=True)
            raise ApiException(f'Internal Server Error: Unable to retrieve product price for product id {product_id}',
                               status_code=500)
