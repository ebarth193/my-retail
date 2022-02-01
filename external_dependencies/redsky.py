import requests
import json
import logging
import properties
from requests import Response
from exceptions.exceptions import ApiException


class Redsky:

    @staticmethod
    def get_product(product_id: str):
        logging.info(f'Attempting to retrieve info for product id {product_id}')
        status_code = None
        try:
            response: Response = requests.get(
                f"{properties.get_property('local', 'REDSKY_URL')}&tcin={product_id}"
            )
            status_code = response.status_code
            response.raise_for_status()
            response_dict = json.loads(response.text)
            logging.info(f'Successfully retrieved info for product id {product_id}')
            return response_dict.get('data', {}).get('product', {}).get('item', {})
        except requests.exceptions.HTTPError as e:
            logging.error(f'HTTPError while retrieving product {product_id}', exc_info=True)
            raise ApiException(f'Unable to retrieve product info for product id {product_id}',
                               status_code=status_code)
        except requests.exceptions.RequestException as e:
            logging.error(f'RequestException while retrieving product {product_id}', exc_info=True)
            raise ApiException(f'Unable to retrieve product info for product id {product_id}',
                               status_code=status_code)
