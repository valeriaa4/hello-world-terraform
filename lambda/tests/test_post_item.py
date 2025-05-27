import json
from create_item.create_item import lambda_handler


def test_post_item_success(mock_dynamodb_table, user_event, registry_body):

    mock_dynamodb_table.put_item.return_value = {}

    response = lambda_handler(registry_body, {})

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Item criado com sucesso."
    assert body["item"]["name"] == "buy milk"
    assert body["item"]["date"] == "2025-12-12"
    assert body["item"]["status"] == "todo"
    assert (
        body["item"]["PK"]
        == f"USER#{user_event['requestContext']['authorizer']['jwt']['claims']['sub']}"
    )
    assert body["item"]["SK"].startswith("ITEM#")

    mock_dynamodb_table.put_item.assert_called_once()


def test_create_item_put_item_failure(mock_dynamodb_table, registry_body):

    mock_dynamodb_table.put_item.side_effect = Exception("simulated put_item error")

    response = lambda_handler(registry_body, {})

    assert response["statusCode"] == 500
    assert "simulated put_item error" in json.loads(response["body"])["error"]


def test_create_item_invalid_date_format(user_event):
    user_event["body"] = json.dumps({"name": "buy milk", "date": "12-12-2025"})

    response = lambda_handler(user_event, {})

    assert response["statusCode"] == 400
    assert "Data inválida" in json.loads(response["body"])["message"]


def test_create_item_missing_fields(user_event):
    user_event["body"] = json.dumps({"name": "", "date": "12-12-2025"})

    response = lambda_handler(user_event, {})

    assert response["statusCode"] == 400
    assert (
        "Campos 'name' e 'date' são obrigatórios."
        in json.loads(response["body"])["message"]
    )


def test_create_item_unauthenticated_user():
    event = {
        "requestContext": {"authorizer": {}},
        "body": json.dumps({"name": "buy milk", "date": "2025-12-12"}),
    }

    response = lambda_handler(event, {})

    assert response["statusCode"] == 401
    assert "Usuário não autenticado" in json.loads(response["body"])["message"]
