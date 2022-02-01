import unittest
from unittest.mock import patch
from services.products import Products
from external_dependencies.redsky import Redsky
from external_dependencies.mongo import Mongo
from models.product import (
    Description,
    Enrichment,
    Image,
    Classification,
    BrandName,
    PriceInfo,
    Item,
    ProductInfo,
    Product
)


class ExceptionsTestCase(unittest.TestCase):
    def setUp(self):
        self.products = Products()
        self.mock_product_id = '123PRODUCTID'
        self.mock_item = Item(
            product_description=Description(
                title='BEST DESCRIPTION',
                downstream_description='TEST DESCRIPTION'
            ),
            enrichment=Enrichment(
                images=Image(primary_image_url='TEST IMAGE URL')),
            product_classification=Classification(
                product_type_name='TEST PRODUCT TYPE', merchandise_type_name='TEST MERCH TYPE'
            ),
            primary_brand=BrandName(name='TEST BRAND'),
            current_price=PriceInfo(value=None, currency_code=None)
        )
        self.mock_price_info = PriceInfo(
            value=10.99,
            currency_code='USD'
        )
        self.mock_missing_price_info = PriceInfo(
            value=None,
            currency_code=None
        )
        self.mock_product_info = ProductInfo(
            tcin=self.mock_product_id,
            item=self.mock_item
        )
        self.mock_product = Product(
            product=(
                ProductInfo(
                    tcin=self.mock_product_id,
                    item=self.mock_item
                )
            )
        )

    @patch.object(Products, 'get_product_details')
    @patch.object(Products, 'get_product_price')
    @patch.object(Products, 'combine_product_info')
    def test_get_product_info_returns_Product(self, mock_combine_product_info, mock_get_product_price,
                                              mock_get_product_details):
        mock_get_product_details.return_value = self.mock_item
        mock_get_product_price.return_value = self.mock_price_info
        mock_combine_product_info.return_value = self.mock_product_info
        result = self.products.get_product_info(self.mock_product_id)
        self.assertEqual(result, self.mock_product)

    @patch.object(Redsky, 'get_product')
    def test_get_product_details_returns_product_result(self, mock_get_product):
        mock_get_product.return_value = self.mock_item.to_dict()
        result = self.products.get_product_details(self.mock_product_id)
        self.assertEqual(result, self.mock_item)

    @patch.object(Mongo, 'get_db_client')
    @patch.object(Mongo, 'get_product_price')
    def test_get_product_price_returns_price_info(self, mock_get_product_price, mock_get_db_client):
        mock_get_product_price.return_value = self.mock_price_info.to_dict()
        result = self.products.get_product_price(self.mock_product_id)
        self.assertEqual(result, self.mock_price_info)

    @patch.object(Mongo, 'get_db_client')
    @patch.object(Mongo, 'get_product_price')
    def test_get_product_price_returns_price_info_with_none(self, mock_get_product_price, mock_get_db_client):
        mock_get_product_price.return_value = self.mock_missing_price_info.to_dict()
        result = self.products.get_product_price(self.mock_product_id)
        self.assertEqual(result, self.mock_missing_price_info)

    def test_combine_product_info_returns_full_product_info(self):
        result = self.products.combine_product_info(self.mock_item, self.mock_missing_price_info, self.mock_product_id)
        self.assertEqual(result.tcin, self.mock_product_id)
        self.assertEqual(result.item, self.mock_item)
