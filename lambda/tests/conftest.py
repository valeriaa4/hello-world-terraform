import pytest
import os
import json
import boto3
from unittest.mock import patch
from moto import mock_aws

os.environ["NOME_TABELA"] = "test_table"


@pytest.fixture
def user_event(sub="test-user-id"):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": sub}}}}}


@pytest.fixture
def registry_body(user_event):
    user_event["body"] = json.dumps({"name": "buy milk", "date": "2025-12-12"})
    return user_event


@pytest.fixture(autouse=True)
def mock_dynamodb_table():
    with patch("create_item.create_item.TABLE") as mock_table:
        yield mock_table


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
                {'AttributeName': 'SK', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        # Itens de exemplo
        table.put_item(Item={
            'PK': 'LIST#123',
            'SK': 'ITEM#1',
            'name': 'Leite',
            'status': 'TODO',
            'listId': '123',
            'itemId': '1'
        })

        table.put_item(Item={
            'PK': 'LIST#123',
            'SK': 'ITEM#2',
            'name': 'Arroz',
            'status': 'DONE',
            'listId': '123',
            'itemId': '2'
        })

        yield table