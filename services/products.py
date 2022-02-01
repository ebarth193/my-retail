from typing import Optional
from external_dependencies.mongo import Mongo
from external_dependencies.redsky import Redsky
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


class Products:

    def get_product_info(self, product_id: str) -> Product:
        product_details: Item = self.get_product_details(product_id)
        product_price: PriceInfo = self.get_product_price(product_id)
        combined_product_info = self.combine_product_info(product_details, product_price, product_id)
        return Product(combined_product_info)

    @staticmethod
    def get_product_details(product_id: str) -> Item:
        result = Redsky().get_product(product_id)
        item = Item(
            product_description=Description(
                title=result.get('product_description').get('title'),
                downstream_description=result.get('product_description').get('downstream_description')
            ),
            enrichment=Enrichment(
                images=Image(primary_image_url=result.get('enrichment').get('images').get('primary_image_url'))
            ),
            product_classification=Classification(
                product_type_name=result.get('product_classification').get('product_type_name'),
                merchandise_type_name=result.get('product_classification').get('merchandise_type_name')
            ),
            primary_brand=BrandName(name=result.get('primary_brand').get('name')),
            current_price=PriceInfo(value=None, currency_code=None)
        )
        return item

    @staticmethod
    def get_product_price(product_id: str) -> PriceInfo:
        mongo = Mongo()
        client = mongo.get_db_client()
        price_info = mongo.get_product_price(client, product_id)
        return PriceInfo(
            value=price_info.get('value') if price_info else None,
            currency_code=price_info.get('currency_code') if price_info else None
        )

    @staticmethod
    def combine_product_info(product_details: Optional[Item], product_price: PriceInfo, product_id: str) -> ProductInfo:
        full_item_details: Item = Item(
            product_description=product_details.product_description,
            enrichment=product_details.enrichment,
            product_classification=product_details.product_classification,
            primary_brand=product_details.primary_brand,
            current_price=product_price
        )
        full_product_info = ProductInfo(
            tcin=product_id,
            item=full_item_details
        )
        return full_product_info
