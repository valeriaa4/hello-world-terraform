import json
import boto3

dynamodb = boto3.resource('dynamodb')
TABLE = dynamodb.Table('MARKET_LIST')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        list_id = body.get('listId')
        item_id = body.get('itemId')
        
        # validação básica
        if not list_id or not item_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'listId e itemId são obrigatórios'})
            }
        
        pk = f"LIST#{list_id}"
        sk = f"ITEM#{item_id}"
        
        try:
            response = TABLE.delete_item(
                Key={
                    'PK': pk,
                    'SK': sk
                },
                ReturnValues='ALL_OLD'  # retorna o item deletado (se existia)
            )
            
            # verifica se o item existia antes da deleção
            deleted_item = response.get('Attributes')
            if not deleted_item:
                return {
                    'statusCode': 404,
                    'body': json.dumps({
                        'message': 'Item não encontrado para exclusão'
                    })
                }

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Item excluído com sucesso',
                    'deletedItem': deleted_item
                })
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Falha ao deletar item',
                    'error': str(e)
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
            'body': json.dumps({'message': 'Erro interno do servidor', 'error': str(e)})
        }