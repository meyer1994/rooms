from datetime import datetime

from pynamodb.models import Model
from pynamodb.attributes import (
    JSONAttribute,
    UnicodeAttribute, 
    UnicodeSetAttribute,
    UTCDateTimeAttribute, 
)


class RoomModel(Model):
    uid = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(default=datetime.utcnow)
    connections = UnicodeSetAttribute(default=set)
    
    class Meta:
        region = 'eu-west-1'
        table_name = 'rooms'


class MessageModel(Model):
    uid = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(default=datetime.utcnow)
    sender = UnicodeSetAttribute(null=False)
    message = JSONAttribute(default=dict)

    class Meta:
        region = 'eu-west-1'
        table_name = 'messages'
