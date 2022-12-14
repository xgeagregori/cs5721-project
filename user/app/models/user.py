from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.attributes import (
    UnicodeAttribute,
    UTCDateTimeAttribute,
    ListAttribute,
    BooleanAttribute,
)

from app.models.chat_message import ChatMessage
from app.models.notification import Notification
from app.models.product_listing import ProductListing
from app.models.profile import ProfileAttribute

import datetime
import os


class UserIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = "username"
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    username = UnicodeAttribute(hash_key=True)


class User(Model):
    class Meta:
        table_name = os.getenv("AWS_USER_TABLE_NAME")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID_LAMBDA")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY_LAMBDA")

    id = UnicodeAttribute(hash_key=True)
    username = UnicodeAttribute()
    email = UnicodeAttribute()
    hashed_password = UnicodeAttribute()
    profile = ProfileAttribute()
    favourites = ListAttribute(of=ProductListing, default=[])
    notifications = ListAttribute(of=Notification, default=[])
    chat_messages = ListAttribute(of=ChatMessage, default=[])
    is_admin = BooleanAttribute()
    is_banned = BooleanAttribute()
    created_at = UTCDateTimeAttribute(default=datetime.datetime.now)

    user_index = UserIndex()
