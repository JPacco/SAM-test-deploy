# functions/update.py
import json
import os
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    user_id = event['pathParameters']['id']
    body = json.loads(event['body'])
    
    try:
        update_expression = "SET "
        expression_values = {}
        
        if 'name' in body:
            update_expression += "name = :n, "
            expression_values[':n'] = body['name']
        
        if 'email' in body:
            update_expression += "email = :e, "
            expression_values[':e'] = body['email']
        
        update_expression = update_expression.rstrip(', ')
        
        response = table.update_item(
            Key={'id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Attributes', {}))
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }