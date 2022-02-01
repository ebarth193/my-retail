from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass
class Description:
    title: str
    downstream_description: str


@dataclass_json
@dataclass
class Image:
    primary_image_url: str


@dataclass_json
@dataclass
class Enrichment:
    images: Image


@dataclass_json
@dataclass
class Classification:
    product_type_name: str
    merchandise_type_name: str


@dataclass_json
@dataclass
class BrandName:
    name: str


@dataclass_json
@dataclass
class PriceInfo:
    value: Optional[float]
    currency_code: Optional[str]


@dataclass_json
@dataclass
class Item:
    product_description: Description
    enrichment: Enrichment
    product_classification: Classification
    primary_brand: BrandName
    current_price: Optional[PriceInfo]


@dataclass_json
@dataclass
class ProductInfo:
    tcin: str
    item: Item


@dataclass_json
@dataclass
class Product:
    product: ProductInfo
