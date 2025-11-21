import os
import json
import boto3
import requests
from decimal import Decimal

# DynamoDB table to store embeddings
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE"))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def lambda_handler(event, context):
    """
    EventBridge event handler for embedding management.
    Event schema:
    {
        "entityType": "organization" | "campaign",
        "id": "string",
        "isDeleted": false,
        "data": {
            "name": "...",
            "description": "...",
            ...
        }
    }
    """
    print("Received event:", json.dumps(event))

    detail = event.get("detail", {})
    entity_type = detail.get("entityType")
    entity_id = detail.get("id")
    data = detail.get("data", {})
    is_deleted = detail.get("isDeleted", False)

    if not entity_type or not entity_id or not data:
        print("Invalid event, missing entityType or id or data")
        return

    # Handle deletion
    if is_deleted:
        try:
            table.delete_item(Key={"target_id": f"{entity_type}_{entity_id}"})
            print(f"Deleted embedding for {entity_type}:{entity_id}")
        except Exception as e:
            print(f"Failed to delete embedding: {e}")
        return

    # Build text for embedding
    text = build_embedding_text(entity_type, data)

    # Compute embedding via OpenAI REST API
    try:
        embedding = get_embedding(text)
    except Exception as e:
        print(f"Failed to get embedding: {e}")
        return

    # Store embedding in DynamoDB
    try:
        table.put_item(
            Item={
                "target_id": f"{entity_type}_{entity_id}",
                "entity_type": entity_type,
                "embedding": [Decimal(str(x)) for x in embedding],
                "source_text": text,
            }
        )
        print(f"Upserted embedding for {entity_type}:{entity_id}")
    except Exception as e:
        print(f"Failed to write embedding to DynamoDB: {e}")


def build_embedding_text(data):
    """
    Concatenate all fields in the data dict into a single string for embedding.
    Each field becomes "key: value" and fields are joined with " | ".
    """
    parts = []
    for k, v in data.items():
        parts.append(f"{k}: {str(v)}")
    return " | ".join(parts)



def get_embedding(text):
    """Call OpenAI embeddings API via HTTP request"""
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "text-embedding-3-small",
        "input": text
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["data"][0]["embedding"]
