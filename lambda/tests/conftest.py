import pytest
import os
import json
import boto3
from unittest.mock import patch
from moto import mock_aws

os.environ["DYNAMODB_TABLE_NAME"] = "test_table"


@pytest.fixture
def user_event(sub="test-user-id"):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": sub}}}}}

@pytest.fixture
def mock_dynamodb_table_get_item():
    with patch("update_item.update_item.table") as mock_table:
        mock_table.get_item.return_value = {"Item": {"PK": "USER#user-123", "SK": "LIST#2025-05-15ITEM#item-1"}}
        yield mock_table

@pytest.fixture
def registry_body(user_event):
    user_event["body"] = json.dumps({"name": "buy milk", "date": "2025-12-12"})
    return user_event


@pytest.fixture(autouse=True)
def mock_dynamodb_table():
    with patch("create_item.create_item.table") as mock_table:
        yield mock_table


@pytest.fixture
def context():
    return {}


@pytest.fixture
def valid_event():
    return {
        "requestContext": {
            "authorizer": {
                "jwt": {
                    "claims": {
                        "sub": "user-123"
                    }
                }
            }
        },
        "pathParameters": {
            "item_id": "item-1"
        },
        "body": json.dumps({
            "name": "Updated name",
            "status": "done",
            "date": "2025-12-12"
        })
    }

@pytest.fixture
def dynamodb_mock():
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName='MARKET_LIST',
            KeySchema=[
                {'AttributeName': 'PK', 'KeyType': 'HASH'},
                {'AttributeName': 'SK', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'PK', 'AttributeType': 'S'},
                {'AttributeName': 'SK', 'AttributeType': 'S'},
                {"AttributeName": "date", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "DateIndex",
                    "KeySchema": [{"AttributeName": "date", "KeyType": "HASH"}],
                    "Projection": {"ProjectionType": "ALL"},
                    "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
                }
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        
        # Itens de exemplo
        table.put_item(Item={
            'PK': 'USER#123',
            'SK': 'LIST#2025-05-15ITEM#1',
            'name': 'Leite',
            'date': '2025-05-15',
            'status': 'TODO',
            'id': '123',
            'item_id': '1'
        })

        table.put_item(Item={
            'PK': 'USER#1234',
            'SK': 'LIST#2025-05-15ITEM#2',
            'name': 'Arroz',
            'date': '2025-05-15',
            'status': 'DONE',
            'id': '1234',
            'item_id': '2'
        })

        yield table
