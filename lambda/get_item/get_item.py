import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
TABLE = dynamodb.Table('MARKET_LIST')

def lambda_handler(event, context):
    try:
        # Parse do body (mesmo padrão da UPDATE)
        body = json.loads(event.get('body', '{}'))
        list_id = body.get('listId')
        item_id = body.get('itemId')
        
        # Validação (igual à UPDATE)
        if not list_id or not item_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'listId e itemId são obrigatórios'})
            }
        
        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"
        
        # Busca o item (equivalente ao get_item da UPDATE)
        response = TABLE.get_item(Key={'PK': pk, 'SK': sk})
        item = response.get('Item')
        
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Item não encontrado'})
            }
        
        # Formata a resposta (mesmo padrão da UPDATE)
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