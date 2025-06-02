import json
import boto3
from datetime import datetime
import os

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ.get('TABLE_NAME', 'MARKET_LIST')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        authorizer = event.get("requestContext", {}).get("authorizer", {})
        claims = authorizer.get("claims") or authorizer.get("jwt", {}).get("claims")

        if not claims or "sub" not in claims:
            return {
                "statusCode": 401,
                "body": json.dumps(
                    {"message": "Usuário não autenticado ou token inválido."}
                ),
            }

        user_id = claims["sub"]
        body = json.loads(event.get("body", "{}"))

        item_id = event.get("pathParameters", {}).get("item_id")
        if item_id:
            item_id = item_id.strip()
        else:    
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "O parâmetro path 'item_id' é obrigatório."}
                ),
            }

        name = body.get("name") # opcional
        date = body.get("date") # obrigatório
        new_date = body.get("new_date")  # opcional, se quiser mudar a data do item
        status = body.get("status") #opcional

        if not date:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "O campo 'date' (data atual) é obrigatório."}),
            }

        if status and status.lower() not in ["todo", "done"]:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "Status inválido. Use 'todo' ou 'done'."}
                ),
            }

        pk = f"USER#{user_id}"
        sk = f"LIST#{date}ITEM#{item_id}"

        response = table.get_item(Key={"PK": pk, "SK": sk})
        item = response.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps(
                    {
                        "message": "Item não encontrado ou acesso não autorizado.",
                        "debug": {"PK": pk, "SK": sk, "response": response},
                    }
                ),
            }

        # se mudar a data, cria novo item e deleta o antigo
        if new_date and new_date != item["date"]:
            try:
                datetime.strptime(new_date, "%Y-%m-%d")
            except ValueError:
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {"message": "Data inválida. Use o formato YYYY-MM-DD."}
                    ),
                }
            new_sk = f"LIST#{new_date}ITEM#{item_id}"
            new_item = item.copy()
            new_item["SK"] = new_sk
            new_item["date"] = new_date
            if name:
                new_item["name"] = name
            if status:
                new_item["status"] = status.lower()
            table.put_item(Item=new_item)
            table.delete_item(Key={"PK": pk, "SK": sk})
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Item atualizado com sucesso.",
                    "item": new_item,
                }),
            }

        # se não mudar a data, atualiza os campos opcionais
        update_expression = []
        expression_values = {}
        expression_names = {}

        if name:
            update_expression.append("#name = :name")
            expression_values[":name"] = name
            expression_names["#name"] = "name"
        if status:
            update_expression.append("#status = :status")
            expression_values[":status"] = status.lower()
            expression_names["#status"] = "status"

        if not update_expression:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Nenhum campo válido para atualizar."}),
            }

        updated = table.update_item(
            Key={"PK": pk, "SK": sk},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeNames=expression_names,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW",
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Item atualizado com sucesso.",
                    "item": updated.get("Attributes", {}),
                }
            ),
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps(
                {"message": "Corpo da requisição inválido. Deve ser JSON válido."}
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Erro ao atualizar item.", "error": str(e)}),
        }
