import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from get_item.get_item import lambda_handler

def mock_event_with_auth_and_date():
    return {
        "queryStringParameters": {"date": "2025-05-15"},
        "requestContext": {
            "authorizer": {
                "jwt": {
                    "claims": {
                        "sub": "user-123"
                    }
                }
            }
        }
    }

def test_get_all_items_success(dynamodb_mock):
    event = mock_event_with_auth_and_date()

    response = lambda_handler(event, None)

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert isinstance(body['items'], list)


def test_missing_date(dynamodb_mock):
    event = mock_event_with_auth_and_date()
    event["queryStringParameters"] = {}

    response = lambda_handler(event, None)

    assert response['statusCode'] == 400
    assert 'obrigatório' in json.loads(response['body'])['message'].lower()


def test_missing_auth(dynamodb_mock):
    event = {
        "queryStringParameters": {"date": "2025-05-15"},
        "requestContext": {}
    }

    response = lambda_handler(event, None)

    assert response['statusCode'] == 401
    assert 'usuário não autenticado' in json.loads(response['body'])['message'].lower()
