import json
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE = dynamodb.Table('MARKET_LIST')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        list_id = body.get('listId')
        item_id = body.get('itemId')
        new_name = body.get('name')
        new_status = body.get('status')
        
        # validação básica
        if not list_id or not item_id:
            return {'statusCode': 400, 'body': 'listId e itemId são obrigatórios'}
        
        if new_status and new_status not in ['TODO', 'DONE']:
            return {'statusCode': 400, 'body': 'status deve ser TODO ou DONE'}
        
        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"
        
        # verifica se o item existe
        if not TABLE.get_item(Key={'PK': pk, 'SK': sk}).get('Item'):
            return {'statusCode': 404, 'body': 'Item não encontrado'}
        
        update_expressions = []
        expression_values = {}
        expression_names = {}
        
        if new_name:
            update_expressions.append('#name = :name')
            expression_values[':name'] = new_name
            expression_names['#name'] = 'name'
            
        if new_status:
            update_expressions.append('#status = :status')
            expression_values[':status'] = new_status
            expression_names['#status'] = 'status'
        
        if not update_expressions:
            return {'statusCode': 400, 'body': 'Nenhum campo para atualizar'}
        
        # atualiza o item
        response = TABLE.update_item(
            Key={'PK': pk, 'SK': sk},
            UpdateExpression='SET ' + ', '.join(update_expressions),
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names if expression_names else None,
            ReturnValues='ALL_NEW'
        )
        
        updated_item = response['Attributes']
        return {
            'statusCode': 200,
            'body': json.dumps({
                'itemId': item_id,
                'listId': list_id,
                'name': updated_item.get('name'),
                'status': updated_item.get('status')
            })
        }
        
    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': 'JSON inválido'}
    except Exception as e:
        return {'statusCode': 500, 'body': 'Erro interno do servidor: ' + str(e)}