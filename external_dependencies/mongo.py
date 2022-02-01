import urllib
import logging
from urllib import parse
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    OperationFailure,
    PyMongoError
)
from properties import get_property
from exceptions.exceptions import ApiException


class Mongo:

    @staticmethod
    def get_db_client():
        logging.info('Attempting to create MongoClient')
        username = urllib.parse.quote_plus(get_property('local', 'MONGO_DB_USER'))
        password = urllib.parse.quote_plus(get_property('local', 'MONGO_DB_PASS'))
        cluster_url = get_property('local', 'MONGO_URL')
        conn_str = f"mongodb+srv://{username}:{password}{cluster_url}"
        try:
            client = MongoClient(conn_str, serverSelectionTimeoutMS=3000)
            database = client[get_property('local', 'MONGO_DB_NAME')]
            return database
        except ConnectionFailure as e:
            logging.error('ConnectionFailure: Unable to create MongoDB client!', exc_info=True)
            raise ApiException("Internal Server Error!", status_code=500) from e
        except PyMongoError as e:
            logging.error('PyMongoError: Unable to create MongoDB client!', exc_info=True)
            raise ApiException("Internal Server Error!", status_code=500) from e

    @staticmethod
    def get_product_price(db_client, product_id: str):
        try:
            logging.info(f"Attempting to retrieve product price for {product_id}")
            price_table = db_client[get_property('local', 'MONGO_DB_PRICE_TABLE')]
            result = price_table.find_one({'product_id': product_id})
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
