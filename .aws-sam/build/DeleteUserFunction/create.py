# functions/create.py
import json
import os
import uuid
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    try:
        body = json.loads(event['body'])
        user_id = str(uuid.uuid4())
        
        item = {
            'id': user_id,
            'name': body.get('name', ''),
            'email': body.get('email', '')
        }
        
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'body': json.dumps({'id': user_id, **item})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }