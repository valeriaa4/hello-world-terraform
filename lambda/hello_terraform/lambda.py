import json

def lambda_handler(event, context):
    
    message = event.get('message', 'Hellow, Terraform!')
    
    return {
        'status': 200,
        'body': message
    }