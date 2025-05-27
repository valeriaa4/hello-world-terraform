import pytest
import os
import json
from unittest.mock import patch

os.environ["NOME_TABELA"] = "test_table"

@pytest.fixture
def user_event(sub="test-user-id"):
    return {"requestContext": {"authorizer": {"jwt": {"claims": {"sub": sub}}}}}

@pytest.fixture
def registry_body(user_event):
    user_event["body"] = json.dumps({
        "name": "buy milk",
        "date": "2025-12-12"
    })
    return user_event

@pytest.fixture(autouse=True)
def mock_dynamodb_table():
    with patch('create_item.create_item.TABLE') as mock_table:
        yield mock_table

