import json
import boto3
import os

TABLE_NAME = os.environ.get('TABLE_NAME', 'MARKET_LIST')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

# Inicializa o cliente DynamoDB com a região correta
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
TABLE = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        # Parse do body 
        body = json.loads(event.get('body', '{}'))
        list_id = body.get('listId')
        item_id = body.get('itemId')
        
        if not list_id or not item_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'listId e itemId são obrigatórios'})
            }
        
        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"
        
        # Busca o item
        response = TABLE.get_item(Key={'PK': pk, 'SK': sk})
        item = response.get('Item')
        
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Item não encontrado'})
            }
        
        # Formata a resposta 
        return {
            'statusCode': 200,
            'body': json.dumps({
                'listId': list_id,
                'itemId': item_id,
                'name': item.get('name'),
                'status': item.get('status'),
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'JSON inválido'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Erro interno do servidor: {str(e)}'})
        }
