import json

def lambda_handler(event, context):
    message = event.get('message', 'Hellow, Terraform!')
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({"message": message}),
        'isBase64Encoded': False
    }
