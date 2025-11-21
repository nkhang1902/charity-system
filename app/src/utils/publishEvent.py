import os
import json
import boto3

eventbridge = boto3.client("events")
EVENT_BUS_NAME = "default"

def publish_entity_event_for_embedding(entity_type, entity_id, data=None, is_deleted=False):
    """
    Publish an EventBridge event when org/campaign is created/updated/deleted
    """
    event_payload = {
        "entityType": entity_type,
        "id": str(entity_id),
        "isDeleted": is_deleted,
        "data": data or {}
    }

    response = eventbridge.put_events(
        Entries=[
            {
                "Source": "myapp.data",
                "DetailType": "EntityChanged",
                "Detail": json.dumps(event_payload),
                "EventBusName": EVENT_BUS_NAME
            }
        ]
    )

    return response
