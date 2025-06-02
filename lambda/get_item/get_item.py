import json
import boto3
import os
from boto3.dynamodb.conditions import Key

TABLE_NAME = os.environ.get('TABLE_NAME', 'MARKET_LIST')

# Inicializa o cliente DynamoDB com a região correta
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
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

        # date como parâmetro path
        date = event.get("queryStringParameters", {}).get("date")
        if not date:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'O parâmetro path "date" é obrigatório.'})
            }
        
        # Busca o item
        response = table.query(
            IndexName="DateIndex",
            KeyConditionExpression=Key('date').eq(date)
        )
        items = response.get('Items', [])
        
        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Nenhum item encontrado'})
            }
        
        # Formata a resposta 
        return {
            'statusCode': 200,
            'body': json.dumps({'items': items})
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
