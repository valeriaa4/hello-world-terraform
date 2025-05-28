import json
import boto3
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
TABLE = dynamodb.Table("MARKET_LIST")


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

        name = body.get("name")
        date = body.get("date")
        status = body.get("status")

        if status and status.lower() not in ["todo", "done"]:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "Status inválido. Use 'todo' ou 'done'."}
                ),
            }

        pk = f"USER#{user_id}"
        sk = f"ITEM#{item_id}"

    
        response = TABLE.get_item(Key={"PK": pk, "SK": sk})
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

        update_expression = []
        expression_values = {}
        expression_names = {}

        if name:
            update_expression.append("#name = :name")
            expression_values[":name"] = name
            expression_names["#name"] = "name"

        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return {
                    "statusCode": 400,
                    "body": json.dumps(
                        {"message": "Data inválida. Use o formato YYYY-MM-DD."}
                    ),
                }
            update_expression.append("#date = :date")
            expression_values[":date"] = date
            expression_names["#date"] = "date"

        if status:
            update_expression.append("#status = :status")
            expression_values[":status"] = status.lower()
            expression_names["#status"] = "status"

        if not update_expression:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Nenhum campo válido para atualizar."}),
            }

        # Realiza o update
        updated = TABLE.update_item(
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
                    "item": updated["Attributes"],
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
