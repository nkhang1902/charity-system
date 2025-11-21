import os
import json
import boto3
import numpy as np
from decimal import Decimal
from boto3.dynamodb.conditions import Attr

# DynamoDB table to store embeddings
dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
table = dynamodb.Table(os.environ.get("DYNAMODB_TABLE"))
# Initialize Bedrock runtime client
bedrock = boto3.client("bedrock-runtime", region_name="ap-southeast-2")
MODEL_ID = os.getenv("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v2:0")

def write_embedding(detail):
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
    print("Received event:", json.dumps(detail))

    # detail = event.get("detail", {})
    entity_type = detail.get("entityType")
    entity_id = detail.get("id")
    data = detail.get("data", {})
    is_deleted = detail.get("isDeleted", False)

    if not entity_type or not entity_id:
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
    else:
        # Build text for embedding
        text = build_embedding_text(data)

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

def get_embedding(text: str) -> list[float]:
    """
    Call Amazon Bedrock to generate embeddings for the given text.
    Returns the embedding as a list of floats.
    """
    # Build the request body
    body = {
        "inputText": text
    }
    body_json = json.dumps(body)

    # Call Bedrock runtime
    kwargs = {
        "modelId": MODEL_ID,
        "body": body_json,
        "contentType": "application/json",
        "accept": "application/json",
    }
    resp = bedrock.invoke_model(**kwargs)

    # Parse response
    resp_body = json.loads(resp["body"].read())
    embedding = resp_body.get("embedding")
    if embedding is None:
        raise Exception("No embedding in Bedrock response: " + json.dumps(resp_body))
    return embedding

def get_all_embedding_from_dynamodb(entity_type):
    try:
         # Scan DynamoDB
        scan_kwargs = {}
        if entity_type:
            scan_kwargs["FilterExpression"] = Attr("entity_type").eq(entity_type)

        response = table.scan(**scan_kwargs)
        items = response.get("Items", [])

        result = []

        for item in items:
            print(item)
            result.append({
                "target_id": item["target_id"],
                "embedding": [to_float(v) for v in item["embedding"]],
            })

        return result
    except Exception as e:
        print(f"Failed to get embedding from DynamoDB: {e}")
        return None

def to_float(x):
    # Decimal → float
    if isinstance(x, Decimal):
        return float(x)
    # {"N": "..."} → float
    if isinstance(x, dict) and "N" in x:
        return float(x["N"])
    # Already float / int
    return float(x)