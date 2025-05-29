import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from get_item.get_item import lambda_handler


def test_get_all_items_success(dynamodb_mock):
    event = {'body': json.dumps({'listId': '123', 'itemId': '1'})}

    response = lambda_handler(event, None)

    assert response['statusCode'] == 200


def test_missing_list_id(dynamodb_mock):
    event = {'body': json.dumps({})}

    response = lambda_handler(event, None)

    assert response['statusCode'] == 400
    assert 'obrigatório' in json.loads(response['body'])['message'].lower()


def test_invalid_json():
    event = {'body': '{invalid_json'}

    response = lambda_handler(event, None)

    assert response['statusCode'] == 400
    assert 'json inválido' in json.loads(response['body'])['message'].lower()
