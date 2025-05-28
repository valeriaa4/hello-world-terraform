import pytest
import os
import json
from unittest.mock import patch

os.environ["NOME_TABELA"] = "test_table"


@pytest.fixture
def user_event(sub="test-user-id"):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": sub}}}}}

@pytest.fixture
def mock_dynamodb_table_get_item():
    with patch("update_item.update_item.TABLE") as mock_table:
        mock_table.get_item.return_value = {"Item": {"PK": "USER#user-123", "SK": "ITEM#item-1"}}
        yield mock_table

@pytest.fixture
def registry_body(user_event):
    user_event["body"] = json.dumps({"name": "buy milk", "date": "2025-12-12"})
    return user_event


@pytest.fixture(autouse=True)
def mock_dynamodb_table():
    with patch("create_item.create_item.TABLE") as mock_table:
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