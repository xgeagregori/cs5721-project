from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute,
    NumberAttribute,
    ListAttribute,
    BooleanAttribute,
)

from app.models.offer import Offer
from app.models.product import ProductAttribute
from app.models.user import UserAttribute

import os


class ProductListing(Model):
    class Meta:
        table_name = os.getenv("AWS_PRODUCT_LISTING_TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID_LAMBDA")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_LAMBDA")

    id = UnicodeAttribute(hash_key=True)
    seller = UserAttribute()
    buyer = UserAttribute(null=True)
    product = ProductAttribute()
    listed_price = NumberAttribute()
    offers = ListAttribute(of=Offer, default=[])
    sold = BooleanAttribute(default=False)
