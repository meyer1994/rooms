import json
import logging
from datetime import datetime

import boto3
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, 
    UnicodeSetAttribute,
    UTCDateTimeAttribute, 
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RoomModel(Model):
    uid = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(default=datetime.utcnow)
    connections = UnicodeSetAttribute(default=set)
    
    class Meta:
        region = 'eu-west-1'
        table_name = 'rooms'


def connect(event, context):
    logger.info(json.dumps(event))
    cid = event['requestContext']['connectionId']

    try:
        logger.info('Fetching room')
        room = RoomModel.get('nice')
    except RoomModel.DoesNotExist:
        logger.info('Room does not exist. Creating new room')
        room = RoomModel('nice', connections={cid})
        room.save()
    
    logger.info('Adding new connection')
    room.update(actions=[
        RoomModel.connections.add({cid})
    ])

    return {}


def disconnect(event, context):
    logger.info(json.dumps(event))
    cid = event['requestContext']['connectionId']

    try:
        logger.info('Fetching room')
        room = RoomModel.get('nice')
    except RoomModel.DoesNotExist:
        logger.info('Room does not exist. Doing nothing')
        return {}
    
    if room.connections == {cid}:
        logger.info('Room only contains current connection. Deleting room')
        room.delete()
        return {}

    logger.info('Removing connection from room')
    room.update(actions=[
        RoomModel.connections.delete({cid})
    ])

    return {}


def message(event, context):
    logger.info(json.dumps(event))
    cid = event['requestContext']['connectionId']

    domain = event['requestContext']['domainName']
    stage = event['requestContext']['stage']

    gtw = boto3.client(
        'apigatewaymanagementapi', 
        endpoint_url=f'https://{domain}/{stage}'
    )

    try:
        logger.info('Fetching room')
        room = RoomModel.get('nice')
    except RoomModel.DoesNotExist:
        logger.info('Room does not exist. Doing nothing')
        return {}

    data = event['body']
    for i in room.connections:
        logger.info('Sending data to connection: %s', i)
        gtw.post_to_connection(ConnectionId=i, Data=data)

    return {}
