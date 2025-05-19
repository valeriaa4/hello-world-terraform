import json
import boto3
from datetime import datetime
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
TABLE = dynamodb.Table('MARKET_LIST')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        nome = body.get('name')
        data = body.get('date')  # formato: 'YYYY-MM-DD'

        if not nome or not data:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Campos 'name' e 'date' são obrigatórios."})
            }
        
        try:
            date_obj = datetime.strptime(data, "%Y-%m-%d")
            pk = date_obj.strftime("%Y%m%d")
        except ValueError:
            return {"statusCode": 400, "body": json.dumps({"message": "Data inválida. Use o formato YYYY-MM-DD."})}

        item_id = str(uuid4())
        sk = f"ITEM#{item_id}"
        pk = f"LIST#{pk}"

        item = {
            "PK": pk,
            "SK": sk,
            "itemId": item_id,
            "name": nome,
            "date": data,
            "status": "todo"
        }

        TABLE.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(SK)"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item criado com sucesso.",
                "item": item
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Erro ao adicionar item.", "error": str(e)})
        }