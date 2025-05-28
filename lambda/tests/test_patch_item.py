import json
import pytest
from unittest.mock import MagicMock, patch
from update_item import update_item


@patch("update_item.update_item.TABLE")
def test_successful_update(mock_table, valid_event, context):
    mock_table.get_item.return_value = {"Item": {"PK": "USER#user-123", "SK": "ITEM#item-1"}}
    mock_table.update_item.return_value = {
        "Attributes": {
            "PK": "USER#user-123",
            "SK": "ITEM#item-1",
            "name": "Updated name",
            "status": "done",
            "date": "2025-12-12"
        }
    }

    response = update_item.lambda_handler(valid_event, context)
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["message"] == "Item atualizado com sucesso."
    assert body["item"]["name"] == "Updated name"


def test_unauthenticated_user(context):
    event = {"requestContext": {}}
    response = update_item.lambda_handler(event, context)
    assert response["statusCode"] == 401


def test_missing_item_id(valid_event, context):
    valid_event["pathParameters"] = {}
    response = update_item.lambda_handler(valid_event, context)
    assert response["statusCode"] == 400
    assert "item_id" in response["body"]


def test_invalid_status(valid_event, context):
    valid_event["body"] = json.dumps({"status": "invalid-status"})
    response = update_item.lambda_handler(valid_event, context)
    body = json.loads(response["body"])
    assert "Status inválido" in body["message"]


@patch("update_item.update_item.TABLE")
def test_item_not_found(mock_table, valid_event, context):
    mock_table.get_item.return_value = {}
    response = update_item.lambda_handler(valid_event, context)
    body = json.loads(response["body"])
    assert "Item não encontrado" in body["message"]



def test_invalid_date_format(mock_dynamodb_table_get_item, valid_event, context):
    valid_event["body"] = json.dumps({"date": "12-12-2025"}) 
    response = update_item.lambda_handler(valid_event, context)
    assert response["statusCode"] == 400

    body = json.loads(response["body"])
    assert "Data inválida" in body["message"]


def test_invalid_json_body(valid_event, context):
    valid_event["body"] = "{invalid json}"
    response = update_item.lambda_handler(valid_event, context)
    body = json.loads(response["body"])
    assert "Corpo da requisição inválido" in body["message"]




@patch("update_item.update_item.TABLE")
def test_no_fields_to_update(mock_table, valid_event, context):
    mock_table.get_item.return_value = {"Item": {"PK": "USER#user-123", "SK": "ITEM#item-1"}}
    valid_event["body"] = json.dumps({})
    response = update_item.lambda_handler(valid_event, context)
    body = json.loads(response["body"])
    assert "Nenhum campo válido" in body["message"]



@patch("update_item.update_item.TABLE", side_effect=Exception("Unexpected error"))
def test_unexpected_exception(mock_table, valid_event, context):
    response = update_item.lambda_handler(valid_event, context)
    assert response["statusCode"] == 500
    assert "Erro ao atualizar item" in response["body"]