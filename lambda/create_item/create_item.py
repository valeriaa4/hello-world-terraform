import json
import boto3
import os
import boto3
from datetime import datetime
from uuid import uuid4

TABLE_NAME = os.environ.get('TABLE_NAME', 'MARKET_LIST')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION) 

TABLE = dynamodb.Table(TABLE_NAME)


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
        nome = body.get("name")
        data = body.get("date")  # formato: 'YYYY-MM-DD'

        if not nome or not data:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "Campos 'name' e 'date' são obrigatórios."}
                ),
            }

        try:
            date_obj = datetime.strptime(data, "%Y-%m-%d")
            pk = date_obj.strftime("%Y%m%d")
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"message": "Data inválida. Use o formato YYYY-MM-DD."}
                ),
            }

        item_id = str(uuid4())
        sk = f"ITEM#{item_id}"
        pk = f"USER#{user_id}"

        item = {"PK": pk, "SK": sk, "name": nome, "date": data, "status": "todo"}

        TABLE.put_item(Item=item, ConditionExpression="attribute_not_exists(SK)")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Item criado com sucesso.", "item": item}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Erro ao adicionar item.", "error": str(e)}),
        }
